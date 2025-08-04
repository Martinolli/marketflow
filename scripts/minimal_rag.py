# minimal_rag_qa.py

import openai
from typing import List
from rag.retriever import chroma_retrieve_top_chunks  # adjust import if needed
from marketflow.marketflow_config_manager import ConfigManager, create_app_config  # adjust import if needed
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_memory_manager import MemoryManager

MEMORY_FILE = ".marketflow/memory/session_default.json"  # Or dynamic per-user/session
memory_manager = MemoryManager(memory_file=MEMORY_FILE)

class MinimalRAGQA:
    def __init__(self, model: str) -> None:

        """Initialize the MinimalRAGQA class.
        Args:
            model (str): The OpenAI model to use for synthesis.
        """
        # Initialize logger
        self.logger = get_logger("MinimalRAGQA")
        # Initialize configuration manager
        self.config_manager = create_app_config(logger=self.logger)
        self.logger.info("Configuration manager initialized.")
        self.model = model or self.config_manager.get_llm_model()
        if not self.model:
            raise ValueError("No LLM model configured.")
         # Log the initialization
        self.logger.info(f"Initialized MinimalRAGQA with model: {self.model}")

        # Initialize memory manager
        self.memory_manager = memory_manager
        self.logger.info(f"Memory manager initialized with file: {MEMORY_FILE}")

    def get_recent_history(self, n=5):
        """Get the last n messages from memory and concatenate them for context.
        Args:
            memory_manager (MemoryManager): The memory manager instance.
            n (int): Number of recent messages to retrieve.
        Returns:
            str: Concatenated string of the last n messages.
        """
        history = self.memory_manager.get_history()[-n:]  # Assumes get_history() returns a list of dicts
        self.logger.debug(f"Recent history: {history}")
        return "\n".join(f"{msg['role']}: {msg['content']}" for msg in history)

    def synthesize_with_openai(self, question: str, chunks: List[dict]) -> str:
        """Synthesizes an answer using OpenAI's LLM based on the provided question and context chunks.
        Args:
            question (str): The user's question.
            chunks (List[dict]): List of context chunks retrieved from the knowledge base.
        Returns:
            str: The synthesized answer from the LLM.
        """
        recent_history = self.get_recent_history(n=5)
        self.logger.debug(f"Recent history for context:\n{recent_history}")
        self.logger.info(f"Synthesizing answer with OpenAI for question: {question}")
        context = "\n\n".join(chunk["text"] for chunk in chunks)
        self.logger.debug(f"Context for synthesis:\n{context}")

        prompt = (
            f"You are an assistant specializing in Wyckoff and Anna Coulling's VPA.\n"
            f"Conversation history:\n{recent_history}\n"
            f"Given this information:\n---\n{context}\n---\n"
            f"**Question:** {question}\n"
            f"Provide a clear, concise answer."
        )

        self.logger.debug(f"Prompt sent to OpenAI:\n{prompt}")
        try:
            # For openai>=1.x
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            answer = response.choices[0].message.content.strip()
            self.logger.info("Received answer from OpenAI.")
            self.logger.debug(f"Answer: {answer}")
        except AttributeError:
            # For openai==0.x
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            answer = response.choices[0].message["content"].strip()
            self.logger.info("Received answer from OpenAI (0.x version).")
            self.logger.debug(f"Answer: {answer}")
        return answer

def main():
    rag_qa = MinimalRAGQA(model=None)  # Use default model from config
    print("🟢 Wyckoff & VPA RAG Q&A (Anna Coulling, etc)")
    print("Ask anything about Wyckoff, VPA, Anna Coulling's book. Type 'quit' to exit.\n")
    rag_qa.logger.info("Started interactive RAG Q&A session.")
    while True:
        user_q = input("You: ").strip()
        if not user_q:
            continue
        # Store user question in memory
        memory_manager.add_message(role="user", content=user_q)
        rag_qa.logger.info(f"Received user question: {user_q}")
        if user_q.lower() in {"quit", "exit"}:
            print("Goodbye!")
            rag_qa.logger.info("User exited the session.")
            break
        # 1. Retrieve top chunks
        top_chunks = chroma_retrieve_top_chunks(user_q, top_k=5)
        rag_qa.logger.debug(f"Top chunks retrieved: {top_chunks}")
        if not top_chunks:
            print("AI: Sorry, I couldn't find anything relevant in the knowledge base.")
            rag_qa.logger.info(f"No relevant chunks found for question: {user_q}")
            continue
        # 2. Synthesize answer with LLM
        try:
            answer = rag_qa.synthesize_with_openai(user_q, top_chunks)
            # Memory management: store the answer
            rag_qa.logger.info(f"Synthesized answer: {answer}")
            memory_manager.add_message(role="assistant", content=answer)
        except Exception as e:
            rag_qa.logger.error("Error during LLM synthesis: %s", e)
            answer = "Sorry, there was an error generating the answer."
        print("\nAI:", answer)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")

