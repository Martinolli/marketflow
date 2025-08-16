"""
# Enhanced RAG Q&A System with Session Management and Source Citations
# and supports retrieving source citations for retrieved chunks.
# and retrieves source citations for retrieved chunks.
This script implements an advanced RAG (Retrieval-Augmented Generation) Q&A system
that allows users to ask questions about financial concepts, particularly focusing on the Wyckoff method
and Volume Price Analysis (VPA) by Anna Coulling. It supports session management,
enhanced memory features, and provides source citations in its answers.
"""

# Initialize OpenAI API key
import openai
import datetime
import uuid
import glob
import os
import re
import numpy as np
from typing import List, Dict, Any, Optional


# We assume these modules are in the python path
from rag.retriever import chroma_retrieve_top_chunks, embed_query
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_memory_manager import MemoryManager
from marketflow.transient_vector_memory import TransientVectorMemory
from rag.embedder import embed_text
import tiktoken


# --- Mock Retriever Function (for demonstration) ---
# This function simulates the retriever returning chunks with source metadata.
# Replace this with your actual retriever function.
def mock_chroma_retrieve_top_chunks(query: str, top_k: int = 6) -> List[Dict[str, Any]]:
    """Mocks the retrieval of chunks with source metadata."""
    print(f"--- (Mock) Retrieving chunks for query: '{query}' ---")
    return [
        {
            "text": "The principle of effort versus result is crucial. High volume on a narrow spread up-bar indicates supply is entering the market, potentially stopping the rise.",
            "metadata": {"source": "A Complete Guide To Volume Price Analysis", "page": 78}
        },
        {
            "text": "A sign of weakness (SOW) often appears as a sharp price increase on high volume, followed by a close well off the highs. This suggests distribution by smart money.",
            "metadata": {"source": "A Complete Guide To Volume Price Analysis", "page": 112}
        },
        {
            "text": "Wyckoff's 'stopping volume' is one of the first reliable indications that a downtrend may be ending. It appears as high volume on a down-bar with a narrow spread.",
            "metadata": {"source": "Wyckoff Methodology Explained", "chapter": 4}
        }
    ]
# --- End Mock ---

class TickerExtractor:
    """Extracts ticker symbols from text, filtering out common words and jargon."""
    def __init__(self):
        # A comprehensive blacklist to avoid misinterpreting common words as tickers.
        self.blacklist = {
            'VPA', 'SOW', 'SOS', 'LPS', 'LPSY', 'PS', 'SC', 'AR', 'ST', 'BC',
            'UTAD', 'SPRING', 'TEST', 'PHASE', 'RSI', 'MACD', 'EMA', 'SMA',
            'NYSE', 'NASDAQ', 'SPX', 'DJI', 'QQQ', 'SPY', 'IWM', 'VIX',
            'FOREX', 'CRYPTO', 'ETF', 'TODAY', 'WEEK', 'MONTH', 'YEAR', 'THE',
            'AND', 'FOR', 'WITH', 'WHAT', 'SHOW', 'TELL', 'ABOUT', 'ANALYSIS',
            'REPORT', 'CHART', 'PRICE', 'VOLUME', 'YOU', 'YOUR', 'ME', 'IS',
            'CAN', 'PLEASE', 'HELP', 'VS', 'BUY', 'SELL', 'HOLD', 'EVENTS'
        }
        self.logger = get_logger("TickerExtractor")

    def extract_tickers(self, text: str) -> List[str]:
        """Extracts potential ticker symbols from a string."""
        # Pattern for standard stock tickers (e.g., AAPL, GOOGL)
        standard_tickers = re.findall(r'\b[A-Z]{1,5}\b', text.upper())
        # Pattern for crypto/forex tickers (e.g., X:BTCUSD, BTC:USD)
        crypto_tickers = re.findall(r'\b[A-Z]+:[A-Z]+\b', text.upper())

        potential_tickers = set(standard_tickers + crypto_tickers)

        # Filter out blacklisted words
        filtered_tickers = [t for t in potential_tickers if t not in self.blacklist]

        if filtered_tickers:
            self.logger.info(f"Extracted tickers: {filtered_tickers} from text: '{text[:100]}...'")
        return sorted(list(set(filtered_tickers)))
class EnhancedRAGQA:
    """
    A dual-source RAG Q&A system using both static and transient memory.
    """

    def __init__(self, session_id: str, model: str = None):
        """
        Initialize the EnhancedRAGQA class for a specific session.
        """
        self.logger = get_logger(f"EnhancedRAGQA_{session_id}")
        self.session_id = session_id

        # --- Configuration and Session Management ---
        self.config_manager = create_app_config(logger=self.logger)
        memory_file = f".marketflow/memory/session_{self.session_id}.json"
        self.memory_manager = MemoryManager(memory_file=memory_file)
        self.model = model or self.config_manager.get_llm_model()
        if not self.model:
            raise ValueError("No LLM model configured.")
        self.logger.info(f"Initialized RAG QA for session '{self.session_id}' using model '{self.model}'")

        # --- Component Initialization ---
        self.ticker_extractor = TickerExtractor()
        
        # Initialize Transient Vector Memory to query recent analysis
        # The embedding dimension must match the model used in marketflow_analysis.py
        self.dim = 1536  # For "text-embedding-3-small"
        self.tvm = TransientVectorMemory(embed_fn=embed_query, dim=self.dim, ttl_seconds=48*3600)
        
        self.namespace = None
        self.namespace_ticker = None
        self.display_name = "Recent Analysis"
        self._load_latest_tvm_namespace()

        # --- System Prompt Setup ---
        if not self.memory_manager.system_messages:
            system_prompt = (
                "You are an expert financial assistant specializing in the Wyckoff method and "
                "Volume Price Analysis (VPA). Your answers should be clear, concise, and directly based on the provided context. "
                "Prioritize the 'RECENT ANALYSIS' section for ticker-specific questions. "
                "Use the 'GENERAL KNOWLEDGE' section for definitions and principles. "
                "Cite your sources using [Source: Recent Analysis] and [Source: Knowledge Base]."
            )
            self.memory_manager.add_system_message(system_prompt)
        self.logger.info("System prompt set in memory.")
    
    def _load_latest_tvm_namespace(self):
        """Finds and loads the most recent TVM namespace file and its associated vector data."""
        report_root = self.config_manager.REPORT_DIR
        candidates = glob.glob(os.path.join(report_root, "**", ".tvm_namespace"), recursive=True)
        if candidates:
            latest_ns_file = max(candidates, key=os.path.getmtime)
            ns_file_dir = os.path.dirname(latest_ns_file)
            tvm_dir = os.path.join(ns_file_dir, ".tvm_store")

            with open(latest_ns_file, "r", encoding="utf-8") as f:
                ns = f.read().strip()

            # Load the actual vector data from the corresponding store directory
            loaded = self.tvm.load_namespace(namespace=ns, dirpath=tvm_dir)
            if not loaded:
                self.logger.error(f"Found namespace file for '{ns}' but failed to load data from {tvm_dir}.")
                return

            self.namespace = ns
            if ns.startswith("batch:"):
                    self.display_name = f"Batch Analysis ({ns.split(':')[1]})"
            else:
                try:
                    self.display_name = f"Single Analysis ({ns.split(':')[-1]})"
                except IndexError:
                    self.display_name = "Recent Analysis"
            
            self.logger.info(f"Successfully loaded TVM namespace '{self.namespace}' ({self.display_name}).")
        else:
            self.logger.warning("No .tvm_namespace file found. Recent analysis retrieval will be disabled.")

    def get_recent_history(self, n=5) -> list:
        """Get the last n messages from memory as a list of dicts for chat context.
        Returns:
            list: List of dicts with 'role' and 'content' keys.
        """
        history = self.memory_manager.get_history()[-n:]  # Assumes get_history() returns a list of dicts
        self.logger.debug(f"Recent history: {history}")
        self.logger.info(f"Retrieved {n} recent messages from memory.")
        # Only include 'role' and 'content' for OpenAI API
        return [{"role": msg["role"], "content": msg["content"]} for msg in history]

    def _format_sources(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Formats the source metadata from chunks into a numbered list for the prompt.
        
        Point 3: RAG Improvements (Chunk Source Metadata)
        
        Args:
            chunks (List[Dict[str, Any]]): The retrieved chunks with metadata.
        Returns:
            str: The formatted source list.
        """
        if not chunks:
            return "No sources provided."

        source_lines = []
        for i, chunk in enumerate(chunks):
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "Unknown Source")
            page = metadata.get("page")
            chapter = metadata.get("chapter")
            
            location = ""
            if page:
                location = f", p. {page}"
            elif chapter:
                location = f", ch. {chapter}"

            source_lines.append(f"[{i+1}] {source}{location}")
        self.logger.debug(f"Formatted sources: {source_lines}")
        self.logger.info(f"Formatted {len(source_lines)} sources for the prompt.")
        
        return "\n".join(source_lines)
    
    def _format_context(self, tvm_chunks: List[Dict], chroma_chunks: List[Dict]) -> str:
        """Formats the retrieved chunks from both sources into a single context string for the LLM."""
        context_parts = []
        
        if tvm_chunks:
            # Use the display name we set during loading
            header = f"--- RECENT ANALYSIS ({self.display_name}) ---"
            tvm_content_lines = []
            for chunk in tvm_chunks:
                # Add the specific ticker from metadata to each chunk's context
                ticker = chunk.get('metadata', {}).get('ticker', 'Unknown Ticker')
                tvm_content_lines.append(f"[Source: Recent Analysis for {ticker}]\n{chunk['text']}")
            
            context_parts.append(f"{header}\n" + "\n\n".join(tvm_content_lines))

        if chroma_chunks:
            chroma_content = "\n\n".join(
                f"[Source: Knowledge Base - {chunk.get('metadata', {}).get('source', 'Unknown')}]\n{chunk['text']}" 
                for chunk in chroma_chunks
            )
            context_parts.append(f"--- GENERAL KNOWLEDGE ---\n{chroma_content}")

        if not context_parts:
            return "No context found."

        return "\n\n".join(context_parts)

    # Build a token-aware, dynamic conversation history based on available context window
    def _estimate_tokens(self, txt: str) -> int:
        try:
            enc = tiktoken.encoding_for_model(self.model)
            return len(enc.encode(txt or ""))
        except Exception:
        # Fallback rough estimate: ~4 chars per token
            return max(1, len((txt or "").strip()) // 4)

    def _ctx_window_for_model(self, model_name: str) -> int:
        # Best-effort mapping; fallback to 8192 if unknown
        mapping = {
        "gpt-4o": 128000,
        "gpt-4o-mini": 128000,
        "gpt-4.1": 128000,
        "gpt-4-turbo": 128000,
        "gpt-3.5-turbo": 16385,
        "text-davinci-003": 4097,
        }
        for k, v in mapping.items():
            if model_name.startswith(k):
                return v
        return 8192
    
    def answer_question(self, question: str) -> str:
        """
        Processes a user question through the dual-source RAG pipeline.
        """
        self.memory_manager.add_message(
            role="user", content=question, timestamp=datetime.datetime.now().isoformat()
        )
        self.logger.info(f"Received user question: {question}")
        
        # 1. Extract Tickers from the question
        tickers = self.ticker_extractor.extract_tickers(question)

        # 2. Retrieve from both sources
        tvm_chunks = []
        # Check if the user is asking about the ticker for which we have recent analysis
        if self.namespace:
            self.logger.info(f"Querying TVM namespace '{self.namespace}' for recent analysis.")
            tvm_chunks = self.tvm.query(self.namespace, question, top_k=6)
            self.logger.info(f"Retrieved {len(tvm_chunks)} chunks from TVM.")
        else:
            self.logger.info("No TVM namespace loaded, skipping recent analysis retrieval.")

        # Always retrieve from the static knowledge base for general context
        self.logger.info("Querying ChromaDB for general knowledge.")
        chroma_chunks = chroma_retrieve_top_chunks(question, top_k=6)
        self.logger.info(f"Retrieved {len(chroma_chunks)} chunks from ChromaDB.")

        if not tvm_chunks and not chroma_chunks:
            self.logger.warning("No relevant chunks found from any source.")
            return "Sorry, I couldn't find any relevant information to answer your question."

        # 3. Augment the prompt with dual-source context
        context = self._format_context(tvm_chunks, chroma_chunks)

        # Reserve tokens for the model's completion and prompt overhead
        context_window = self._ctx_window_for_model(self.model)
        reserved_for_completion = 1024  # matches max_tokens below
        prompt_overhead = 600  # safety buffer for formatting, system text, etc.

        # Estimate tokens consumed by the context and question
        context_tokens = self._estimate_tokens(context)
        question_tokens = self._estimate_tokens(question)

        # Budget for history messages
        history_budget = max(
            0,
            context_window - reserved_for_completion - prompt_overhead - context_tokens - question_tokens,
        )

        # Accumulate messages from the end until we hit the budget
        full_history = self.memory_manager.get_history()
        role_content_history = [{"role": m["role"], "content": m["content"]} for m in full_history[:-1]]

        tokens_used = 0
        selected = []
        for msg in reversed(role_content_history):
            msg_tokens = self._estimate_tokens(msg["content"]) + 8  # small per-message overhead
            if tokens_used + msg_tokens > history_budget and selected:
                break
            if tokens_used + msg_tokens > history_budget:
            # If nothing selected yet and even this one doesn't fit, skip it
                break
            selected.append(msg)
            tokens_used += msg_tokens

        history = list(reversed(selected))
        self.logger.info(f"Dynamically selected {len(history)} messages for conversation history ({tokens_used} tokens).")

        augmented_prompt = (
            "Please answer the question based on the conversation history and the context provided below.\n\n"
            "<context>\n{context}\n</context>\n\n"
            "<question>{question}</question>\n\n"
            "Answer:"
        ).format(context=context, question=question)

        # The 'history' list is prepended here, which is the correct OpenAI format.
        messages_for_api = history + [{"role": "user", "content": augmented_prompt}]
        self.logger.debug(f"Payload for OpenAI: {messages_for_api}")
        
        # 4. Generate
        try:
            client = openai.OpenAI()
            response_stream = client.chat.completions.create(
                model=self.model,
                messages=messages_for_api,
                max_tokens=1024,
                temperature=0.5,
                stream=True  # Enable streaming
            )

            full_answer = ""
            # In a web UI, you would yield these chunk. In the console, we print them.
            print("\nAI: ", end="", flush=True)
            for chunk in response_stream:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    full_answer += content

            answer = full_answer.strip()
            print() # New line after AI response
            self.logger.info("Successfully generated answer from OpenAI.")
        except Exception as e:
            self.logger.error(f"Error during OpenAI API call: {e}", exc_info=True)
            answer = "I'm sorry, but I encountered an error while generating a response."

        # Store assistant's response in memory
        if answer:
            self.memory_manager.add_message(
                role="assistant", content=answer, timestamp=datetime.datetime.now().isoformat()
            )
        return answer

def main():
    """Main interactive loop for the Q&A session."""
    session_id = input("Enter a session ID (or press Enter for a new one): ").strip()
    if not session_id:
        session_id = str(uuid.uuid4())[:8]
    
    print(f"\n🟢 Welcome to the Enhanced RAG Q&A Session! (ID: {session_id})")
    print("Special commands: '/quit', '/clear', '/history', '/repair'")

    try:
        rag_qa = EnhancedRAGQA(session_id=session_id)
    except ValueError as e:
        print(f"Fatal Error: {e}")
        return

    while True:
        user_q = input("\nYou: ").strip()
        if not user_q:
            continue
        if user_q.lower() == '/quit':
            print("Goodbye!")
            break
        elif user_q.lower() == '/clear':
            rag_qa.memory_manager.clear_memory()
            print("Session history has been cleared.")
            continue
        elif user_q.lower() == '/history':
            history = rag_qa.memory_manager.get_history(limit=20)
            print("\n--- Session History ---")
            for msg in history[-20:]:
                print(f"- {msg['role']}: {msg['content'][:80]}...")
            print("-----------------------\n")
            continue
        elif user_q.lower() == '/repair':
            print("\n--- Repairing Conversation ---")
            stats = rag_qa.memory_manager.repair_conversation()
            print(f"Repair complete. Stats: {stats}")
            continue

        answer = rag_qa.answer_question(user_q)
        print(f"\nAI: {answer}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")