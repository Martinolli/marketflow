# minimal_rag_qa.py

from xml.parsers.expat import model
from xmlrpc import client
import openai
from rag.retriever import chroma_retrieve_top_chunks  # adjust import if needed
from marketflow.marketflow_config_manager import ConfigManager, create_app_config  # adjust import if needed
from marketflow.marketflow_logger import get_logger


class MinimalRAGQA:
    def __init__(self, model: str) -> None:

        """Initialize the MinimalRAGQA class.
        Args:
            model (str): The OpenAI model to use for synthesis.
        """
        # Initialize configuration and model
        config = ConfigManager()
        model = config.get_llm_model()
        if not model:
            raise ValueError("No LLM model configured. Please set a valid OpenAI model in the configuration.")
        self.model = model
        # Initialize logger
        self.logger = get_logger("MinimalRAGQA")
        # Log the initialization
        self.logger.info(f"Initialized MinimalRAGQA with model: {self.model}")
        # Initialize configuration manager
        self.config_manager = create_app_config(logger=self.logger)
        self.logger.info("Configuration manager initialized.")

    def synthesize_with_openai(self, question: str, chunks: list[dict]) -> str:
        self.logger.info("Synthesizing answer with OpenAI for question: %s", question)
        context = "\n\n".join(chunk["text"] for chunk in chunks)
        self.logger.debug("Context for synthesis:\n%s", context)
        prompt = (
            f"You are an assistant specializing in Wyckoff and Anna Coulling's VPA. "
            f"Given this information:\n---\n{context}\n---\n"
            f"Answer this question in a clear and direct way: '{question}'"
        )
        self.logger.debug("Prompt sent to OpenAI:\n%s", prompt)
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.6,
        )
        answer = response.choices[0].message.content.strip()
        self.logger.info("Received answer from OpenAI.")
        self.logger.debug("Answer: %s", answer)
        return answer

rag_qa = MinimalRAGQA(model=model)
synthesize_with_openai = rag_qa.synthesize_with_openai


def main():
    print("🟢 Wyckoff & VPA RAG Q&A (Anna Coulling, etc)")
    print("Ask anything about Wyckoff, VPA, Anna Coulling's book. Type 'quit' to exit.\n")
    rag_qa.logger.info("Started interactive RAG Q&A session.")
    while True:
        user_q = input("You: ").strip()
        rag_qa.logger.info("Received user question: %s", user_q)
        if user_q.lower() in {"quit", "exit"}:
            print("Goodbye!")
            rag_qa.logger.info("User exited the session.")
            break
        # 1. Retrieve top chunks
        top_chunks = chroma_retrieve_top_chunks(user_q, top_k=5)
        rag_qa.logger.debug("Top chunks retrieved: %s", top_chunks)
        if not top_chunks:
            print("AI: Sorry, I couldn't find anything relevant in the knowledge base.")
            rag_qa.logger.info("No relevant chunks found for question: %s", user_q)
            continue
        # 2. Print context for transparency (later: send to LLM)
        print("\nAI: Top context from Anna Coulling/Wyckoff corpus:\n" + "-"*60)
        for i, chunk in enumerate(top_chunks, 1):
            meta = chunk.get("metadata", {})
            print(f"\nChunk {i}:")
            print(f"Source: {meta.get('source', '?')} | Page: {meta.get('page', '?')}")
            print(chunk["text"][:400].strip())
            rag_qa.logger.debug("Chunk %d: Source: %s, Page: %s, Text: %s", i, meta.get('source', '?'), meta.get('page', '?'), chunk["text"][:400].strip())
        print("-"*60)
        # 3. Synthesize answer with LLM
        answer = synthesize_with_openai(user_q, top_chunks)
        print("\nAI:", answer)
        rag_qa.logger.info("Answer provided to user: %s", answer)

if __name__ == "__main__":
    main()
