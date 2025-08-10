# marketflow/transient_vector_memory.py
from __future__ import annotations
from typing import Dict, Any, List, Optional
import time, uuid, hashlib
import json, os
import faiss
import numpy as np
import re

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

class TVMStore:
    """FAISS + in-memory metadata, scoped by namespace."""
    def __init__(self, dim: int):

        self.logger = get_logger("TVM_Store")
        self.config_manager = create_app_config(logger=self.logger)
        self.dim = dim
        self.index_by_ns: Dict[str, faiss.IndexFlatIP] = {}
        self.meta_by_ns: Dict[str, List[Dict[str,Any]]] = {}

    def _get_or_create(self, ns: str):
        if ns not in self.index_by_ns:
            self.index_by_ns[ns] = faiss.IndexFlatIP(self.dim)
            self.meta_by_ns[ns] = []
            self.logger.info(f"Created new TVM namespace: {ns}")
        return self.index_by_ns[ns], self.meta_by_ns[ns]

    def add(self, ns: str, vecs: np.ndarray, metas: List[Dict[str,Any]]):
        index, metas_list = self._get_or_create(ns)
        self.logger.debug(f"Adding {len(vecs)} vectors to TVM namespace: {ns}")
        index.add(vecs.astype(np.float32))
        metas_list.extend(metas)
        self.logger.info(f"Added {len(vecs)} vectors to TVM namespace: {ns}")

    def search(self, ns: str, qvec: np.ndarray, top_k: int):
        if ns not in self.index_by_ns or self.index_by_ns[ns].ntotal == 0:
            return []
        index, metas_list = self.index_by_ns[ns], self.meta_by_ns[ns]
        self.logger.debug(f"Searching TVM namespace: {ns} with query vector of shape {qvec.shape}")
        D, I = index.search(qvec.astype(np.float32), top_k)
        out = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1: continue
            m = metas_list[idx]
            m = dict(m)
            m["cosine"] = float(score)
            out.append(m)
        self.logger.info(f"Search results for TVM namespace: {ns}, found {len(out)} entries")
        return out

    def prune_older_than(self, ns: str, cutoff_ts: int):
        if ns not in self.meta_by_ns: return
        index, metas = self.index_by_ns[ns], self.meta_by_ns[ns]
        keep = [i for i, m in enumerate(metas) if m.get("created_at", 0) >= cutoff_ts]
        if len(keep) == len(metas): return
        # rebuild smaller index
        new_index = faiss.IndexFlatIP(self.dim)
        new_metas = [metas[i] for i in keep]
        vecs = np.vstack([m["vector"] for m in new_metas]).astype(np.float32) if new_metas else np.zeros((0,self.dim), np.float32)
        self.logger.info(f"Pruning TVM namespace: {ns}, keeping {len(new_metas)} out of {len(metas)} entries")
        if len(new_metas): new_index.add(vecs)
        self.index_by_ns[ns], self.meta_by_ns[ns] = new_index, new_metas
        self.logger.debug(f"Pruned TVM namespace: {ns}, now has {len(new_metas)} entries")

class TransientVectorMemory:
    def __init__(self, embed_fn, dim: int, ttl_seconds: int = 24*3600, half_life_h: int = 12):

        self.logger = get_logger("Transient_Vector_Memory")
        self.config_manager = create_app_config(logger=self.logger)
        self.embed_fn = embed_fn
        self.dim = dim
        self.store = TVMStore(dim)
        self.ttl = ttl_seconds
        self.half_life_h = half_life_h

    def _now(self): return int(time.time())
    def _hash(self, text: str): return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _chunk(self, text: str, size=900, overlap=150):
        self.logger.debug(f"Chunking text of length {len(text)} into size {size} with overlap {overlap}")
        words = text.split()
        i, out = 0, []
        while i < len(words):
            out.append(" ".join(words[i:i+size]))
            i += size - overlap
        return out

    def upsert_text(self, namespace: str, report_id: str, text: str, meta: Dict[str,Any]):
        th = self._hash(text)
        chunks = self._chunk(text)
        metas, vecs = [], []
        now = self._now()

        for ch in chunks:
            v = self.embed_fn(ch)  # -> List[float] length == dim
            if len(v) != self.dim:
                raise ValueError(f"Embedding dim {len(v)} != expected {self.dim}")
            metas.append({
                "chunk_id": str(uuid.uuid4()),
                "namespace": namespace,
                "report_id": report_id,
                "text": ch,
                "vector": np.array(v, dtype=np.float32),
                "text_hash": th,
                "created_at": now,
                **meta
            })
            vecs.append(v)
        self.store.add(namespace, np.array(vecs, dtype=np.float32), metas)
        self.logger.info(f"Upserted {len(chunks)} chunks into TVM namespace: {namespace}")
        # prune expired
        self.store.prune_older_than(namespace, now - self.ttl)
        self.logger.debug(f"Pruned TVM namespace: {namespace}, now has {len(self.store.meta_by_ns[namespace])} entries")

    def query(self, namespace: str, query_text: str, top_k: int = 5) -> List[Dict[str,Any]]:
        qv = np.array([self.embed_fn(query_text)], dtype=np.float32)
        self.logger.debug(f"Querying TVM namespace: {namespace} with vector shape {qv.shape}")
        hits = self.store.search(namespace, qv, top_k*2 or 5)
        # recency boost
        now = self._now()
        def recency(created_at):
            age_h = max(1.0, (now - created_at)/3600.0)
            return np.exp(-age_h/self.half_life_h)
        for h in hits:
            h["score"] = 0.70*h["cosine"] + 0.30*recency(h.get("created_at", now))
            self.logger.debug(f"Hit: {h}")
        return sorted(hits, key=lambda x: x["score"], reverse=True)[:top_k]
    
    import re, json, os, numpy as np, faiss

    def _ns_to_filename(self, namespace: str) -> str:
        # keep the in-memory namespace as-is; only sanitize the filename
        # allow [A-Za-z0-9_.-]; replace others with '_'
        return re.sub(r'[^A-Za-z0-9_.-]+', '_', namespace)

    def save_namespace(self, namespace: str, dirpath: str):
        os.makedirs(dirpath, exist_ok=True)
        fname = self._ns_to_filename(namespace)
        idx_path = os.path.join(dirpath, f"{fname}.faiss")
        meta_path = os.path.join(dirpath, f"{fname}.meta.json")

        index, metas = self.store._get_or_create(namespace)
        faiss.write_index(index, idx_path)

        serializable = []
        for m in metas:
            c = dict(m)
            # ensure contiguous float32 vectors
            c["vector"] = np.ascontiguousarray(c["vector"], dtype=np.float32).tolist()
            serializable.append(c)

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False)

    def load_namespace(self, namespace: str, dirpath: str) -> bool:
        fname = self._ns_to_filename(namespace)
        idx_path = os.path.join(dirpath, f"{fname}.faiss")
        meta_path = os.path.join(dirpath, f"{fname}.meta.json")
        if not (os.path.exists(idx_path) and os.path.exists(meta_path)):
            return False

        index = faiss.read_index(idx_path)
        with open(meta_path, "r", encoding="utf-8") as f:
            metas = json.load(f)
        for m in metas:
            m["vector"] = np.ascontiguousarray(np.array(m["vector"], dtype=np.float32))
        self.store.index_by_ns[namespace] = index
        self.store.meta_by_ns[namespace] = metas
        return True
