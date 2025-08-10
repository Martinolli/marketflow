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
from typing import List, Dict, Any
import glob, os


# We assume these modules are in the python path
from rag.retriever import chroma_retrieve_top_chunks
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_memory_manager import MemoryManager

# --- Mock Retriever Function (for demonstration) ---
# This function simulates the retriever returning chunks with source metadata.
# Replace this with your actual retriever function.
def mock_chroma_retrieve_top_chunks(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
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
class EnhancedRAGQA:
    """
    An enhanced RAG Q&A system that supports sessions, uses advanced memory features,
    and provides source citations in its answers.
    """

    def __init__(self, session_id: str, model: str = None):
        """
        Initialize the EnhancedRAGQA class for a specific session.

        Args:
            session_id (str): A unique identifier for the user or conversation session.
            model (str, optional): The OpenAI model to use. Defaults to config.
        """
        self.logger = get_logger(f"EnhancedRAGQA_{session_id}")
        self.session_id = session_id
        
        # Point 1: Session & User Management
        # The memory file is now dynamically created based on the session_id.
        memory_file = f".marketflow/memory/session_{self.session_id}.json"

        # The MemoryManager is now an instance variable, tied to the session.
        self.memory_manager = MemoryManager(memory_file=memory_file)
        self.logger.info(f"Initialized RAG QA for session '{self.session_id}' with memory at '{memory_file}'")

        # Configuration
        self.config_manager = create_app_config(logger=self.logger)
        self.model = model or self.config_manager.get_llm_model()
        if not self.model:
            raise ValueError("No LLM model configured.")
        self.logger.info(f"Using LLM model: {self.model}")

        # Point 2: Enhanced Conversation Memory (System Messages)
        # Set a system message once per session to guide the assistant's behavior.
        # We check if system messages are empty to avoid adding it on every run.
        if not self.memory_manager.system_messages:
            system_prompt = (
                "You are an expert financial assistant specializing in the Wyckoff method and "
                "Anna Coulling's Volume Price Analysis (VPA). Your answers should be clear, concise, and "
                "directly based on the provided context. When you use information from a source, "
                "cite it using the format [1], [2], etc., corresponding to the source list."
            )
            self.memory_manager.add_system_message(system_prompt)
        self.logger.info("System prompt added to memory.")

        report_root = self.config_manager.REPORT_DIR
        candidates = glob.glob(os.path.join(report_root, "**", ".tvm_namespace"), recursive=True)
        if candidates:
            latest = max(candidates, key=os.path.getmtime)
            with open(latest, "r", encoding="utf-8") as f:
                self.namespace = f.read().strip()
            self.logger.info(f"Loaded TVM namespace: {self.namespace}")

    
    def get_recent_history(self, n=5) -> str:
        """Get the last n messages from memory and concatenate them for context.
        Args:
            memory_manager (MemoryManager): The memory manager instance.
            n (int): Number of recent messages to retrieve.
        Returns:
            str: Concatenated string of the last n messages.
        """
        history = self.memory_manager.get_history()[-n:]  # Assumes get_history() returns a list of dicts
        self.logger.debug(f"Recent history: {history}")
        self.logger.info(f"Retrieved {n} recent messages from memory.")
        return "\n".join(f"{msg['role']}: {msg['content']}" for msg in history)

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

    def answer_question(self, question: str) -> str:
        """
        Processes a user question through the RAG pipeline: retrieve, augment, generate.

        Args:
            question (str): The user's question.

        Returns:
            str: The AI-generated answer.
        """
        # Point 2: Enhanced Conversation Memory (Store Metadata)
        # We can add arbitrary metadata, like a timestamp, to each message.
        timestamp = datetime.datetime.now().isoformat()
        self.memory_manager.add_message(role="user", content=question, timestamp=timestamp)
        self.logger.info(f"Received user question: {question}")
        
        # 1. Retrieve
    
        top_chunks = chroma_retrieve_top_chunks(question, top_k=6)
        
        if not top_chunks:
            self.logger.warning("No relevant chunks found.")
            return "Sorry, I couldn't find any relevant information in the knowledge base to answer your question."

        # 2. Augment
        context = "\n\n".join(chunk["text"] for chunk in top_chunks)
        formatted_sources = self._format_sources(top_chunks)
        
        # Get history from memory manager. It will be combined with the system prompt.
        history = self.memory_manager.get_history(limit=5)

        # The final prompt message is augmented with the retrieved context and sources.
        augmented_prompt = (
            "Please answer the following question based on the conversation history and the context provided below.\n\n"
            f"--- CONTEXT ---\n{context}\n\n"
            f"--- SOURCES ---\n{formatted_sources}\n\n"
            f"--- QUESTION ---\n{question}"
        )
        
        # Add the augmented user message to the history for the API call
        history.append({"role": "user", "content": augmented_prompt})
        # Log the payload for debugging purposes
        self.logger.debug(f"Payload for OpenAI: {history}")

        # 3. Generate
        try:
            # For openai>=1.x
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": augmented_prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            answer = response.choices[0].message.content.strip()
            self.logger.info("Successfully synthesized answer from OpenAI.")
        except AttributeError:
            # For openai==0.x
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": augmented_prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            answer = response.choices[0].message.content.strip()
            self.logger.info("Received answer from OpenAI. (0.x version)")
            self.logger.debug(f"Answer: {answer}")
        # Handle potential errors in the API call
        
        except Exception as e:
            self.logger.error(f"Error during OpenAI API call: {e}", exc_info=True)
            answer = "I'm sorry, but I encountered an error while generating a response."

        # Store the assistant's response in memory with a timestamp
        if answer:
            self.logger.info(f"Storing assistant's answer: {answer}")
            # Point 4: Enhanced Memory - Store assistant's response with metadata
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
            for msg in history:
                print(f"- {msg['role']}: {msg['content'][:80]}...")
            print("-----------------------\n")
            continue
        # Point 2: Enhanced Memory - Leveraging validation and repair
        elif user_q.lower() == '/repair':
            print("\n--- Repairing Conversation ---")
            stats = rag_qa.memory_manager.repair_conversation()
            print(f"Repair complete. Stats: {stats}")
            continue

        answer = rag_qa.answer_question(user_q)

        # Store the assistant's response in memory with a timestamp
        rag_qa.memory_manager.add_message(
                role="assistant", 
                content=answer, 
                timestamp=datetime.datetime.now().isoformat()
            )
        print(f"\nAI: {answer}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")