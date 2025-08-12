# repair_tvm_namespace.py
import os, json
from pathlib import Path
from marketflow.transient_vector_memory import TransientVectorMemory
from rag.embedder import embed_text  # your wrapper

def main(run_dir: str):
    ns_path = Path(run_dir) / ".tvm_namespace"
    tvm_dir = Path(run_dir) / ".tvm_store"
    if not ns_path.exists():
        raise SystemExit(f"No namespace file at {ns_path}")

    namespace = ns_path.read_text(encoding="utf-8").strip()
    tvm = TransientVectorMemory(embed_fn=embed_text, dim=1536, ttl_seconds=24*3600)
    loaded = tvm.load_namespace(namespace, str(tvm_dir))
    print(f"Loaded TVM: {loaded}  namespace={namespace}")

    # build a proper narrative from your saved files
    ticker = Path(run_dir).name
    narrative = ""
    p_txt = Path(run_dir) / f"{ticker}_summary.txt"
    if p_txt.exists():
        narrative = p_txt.read_text(encoding="utf-8").strip()

    if not narrative:
        p_llm = Path(run_dir) / f"{ticker}_llm_analysis.json"
        if p_llm.exists():
            try:
                data = json.loads(p_llm.read_text(encoding="utf-8"))
                narrative = data.get("narrative") or data.get("summary") or data.get("analysis_text") or ""
            except Exception:
                pass

    if not isinstance(narrative, str) or len(narrative.split()) < 15:
        narrative = f"{ticker}: AMD run repair narrative — analysis available in reports."

    tvm.upsert_text(namespace, f"{ticker}_repair", narrative, meta={"source":"repair","ticker":ticker})
    tvm.save_namespace(namespace, str(tvm_dir))
    print("TVM repaired & saved ✅")

if __name__ == "__main__":
    # Example: python repair_tvm_namespace.py "...\2025-08-10\AMD"
    import sys
    if len(sys.argv) != 2:
        print("Usage: python repair_tvm_namespace.py <run_dir_for_ticker>")
        raise SystemExit(1)
    main(sys.argv[1])
