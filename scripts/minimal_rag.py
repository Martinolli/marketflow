# minimal_rag_qa.py

import openai
import argparse
import os
from typing import List, Optional, Dict, Any
from rag.retriever import chroma_retrieve_top_chunks  # adjust import if needed
from marketflow.marketflow_config_manager import create_app_config  # adjust import if needed
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_memory_manager import MemoryManager

class MinimalRAGQA:
    def __init__(self, model: str, session_id: str = "default", system_prompt: Optional[str] = None) -> None:
        """Initialize the MinimalRAGQA class.
        Args:
            model (str): The OpenAI model to use for synthesis.
            session_id (str): Session identifier for memory management.
            system_prompt (str, optional): Custom system prompt to initialize conversation.
        """
        # Initialize logger
        self.logger = get_logger("MinimalRAGQA")
        
        # Initialize configuration manager
        self.config_manager = create_app_config(logger=self.logger)
        self.logger.info("Configuration manager initialized.")
        
        # Set up model
        self.model = model or self.config_manager.get_llm_model()
        if not self.model:
            raise ValueError("No LLM model configured.")
        self.logger.info(f"Initialized MinimalRAGQA with model: {self.model}")
        
        # Set up session-based memory
        self.session_id = session_id
        memory_file = f".marketflow/memory/session_{session_id}.json"
        
        try:
            self.memory_manager = MemoryManager(memory_file=memory_file)
            self.logger.info(f"Memory manager initialized with file: {memory_file}")
        except Exception as e:
            self.logger.error(f"Failed to initialize memory manager: {e}")
            raise
        
        # Initialize with system prompt if provided
        if system_prompt:
            self._initialize_system_prompt(system_prompt)
        else:
            # Default system prompt
            default_prompt = (
                "You are an expert assistant specializing in Wyckoff Method and "
                "Anna Coulling's Volume Price Analysis (VPA). You provide clear, "
                "accurate answers based on the provided context and conversation history."
            )
            self._initialize_system_prompt(default_prompt)

    def _initialize_system_prompt(self, system_prompt: str) -> None:
        """Initialize system prompt for the session."""
        try:
            self.memory_manager.add_system_message(system_prompt)
            self.logger.info("System prompt initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize system prompt: {e}")

    def get_recent_history(self, n: int = 5) -> str:
        """Get the last n messages from memory and concatenate them for context.
        Args:
            n (int): Number of recent messages to retrieve.
        Returns:
            str: Concatenated string of the last n messages.
        """
        try:
            history = self.memory_manager.get_history(limit=n)
            # Filter out system messages for context building
            conversation_history = [msg for msg in history if msg.get('role') != 'system']
            self.logger.debug(f"Retrieved {len(conversation_history)} recent messages")
            return "\n".join(f"{msg['role']}: {msg['content']}" for msg in conversation_history[-n:])
        except Exception as e:
            self.logger.error(f"Error retrieving recent history: {e}")
            return ""

    def synthesize_with_openai(self, question: str, chunks: List[dict]) -> str:
        """Synthesizes an answer using OpenAI's LLM based on the provided question and context chunks.
        Args:
            question (str): The user's question.
            chunks (List[dict]): List of context chunks retrieved from the knowledge base.
        Returns:
            str: The synthesized answer from the LLM.
        """
        try:
            # Get recent history for context
            recent_history = self.get_recent_history(n=5)
            self.logger.debug(f"Recent history for context:\n{recent_history}")
            self.logger.info(f"Synthesizing answer with OpenAI for question: {question}")
            
            # Build context with metadata
            context_parts = []
            source_info = []
            
            for i, chunk in enumerate(chunks, 1):
                chunk_text = chunk.get("text", "")
                metadata = chunk.get("metadata", {})
                source = metadata.get("source", "Unknown")
                page = metadata.get("page", "Unknown")
                
                context_parts.append(f"[Source {i}: {source}, Page {page}]\n{chunk_text}")
                source_info.append(f"Source {i}: {source} (Page {page})")
            
            context = "\n\n".join(context_parts)
            self.logger.debug(f"Context for synthesis (with metadata):\n{context}")

            # Build comprehensive prompt with conversation history and sources
            prompt = (
                f"Based on the following sources and conversation history, provide a clear and accurate answer.\n\n"
                f"Conversation History:\n{recent_history}\n\n"
                f"Knowledge Base Context:\n{context}\n\n"
                f"Current Question: {question}\n\n"
                f"Please provide a comprehensive answer based on the sources above. "
                f"When referring to specific information, you may mention the source if relevant."
            )

            self.logger.debug(f"Prompt sent to OpenAI:\n{prompt}")
            
            # Make API call with error handling
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
                self.logger.info("Successfully received answer from OpenAI.")
                self.logger.debug(f"Answer: {answer}")
                
                # Store source information for potential later use
                self.last_sources = source_info
                
            except AttributeError:
                # For openai==0.x
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=512,
                    temperature=0.6,
                )
                answer = response.choices[0].message["content"].strip()
                self.logger.info("Successfully received answer from OpenAI (0.x version).")
                self.logger.debug(f"Answer: {answer}")
                
                # Store source information for potential later use
                self.last_sources = source_info
                
            return answer
            
        except Exception as e:
            self.logger.error(f"Error during LLM synthesis: {e}")
            raise

    def display_sources(self) -> str:
        """Display the sources from the last query."""
        if not hasattr(self, 'last_sources') or not self.last_sources:
            return "No sources available from the last query."
        
        sources_text = "📚 Sources from last query:\n"
        for source in self.last_sources:
            sources_text += f"  • {source}\n"
        return sources_text

    def clear_memory(self) -> str:
        """Clear conversation memory."""
        try:
            self.memory_manager.clear_memory()
            self.logger.info("Memory cleared successfully.")
            return "🧹 Conversation memory cleared."
        except Exception as e:
            self.logger.error(f"Error clearing memory: {e}")
            return f"❌ Error clearing memory: {e}"

    def repair_memory(self) -> str:
        """Repair conversation memory."""
        try:
            repair_stats = self.memory_manager.repair_conversation()
            self.logger.info(f"Memory repaired: {repair_stats}")
            return f"🔧 Memory repaired. Removed {repair_stats.get('messages_removed', 0)} problematic messages."
        except Exception as e:
            self.logger.error(f"Error repairing memory: {e}")
            return f"❌ Error repairing memory: {e}"

    def get_memory_stats(self) -> str:
        """Get memory statistics."""
        try:
            stats = self.memory_manager.get_memory_stats()
            stats_text = f"📊 Memory Statistics for session '{self.session_id}':\n"
            stats_text += f"  • Total messages: {stats.get('total_messages', 0)}\n"
            stats_text += f"  • System messages: {stats.get('system_messages', 0)}\n"
            stats_text += f"  • Memory file: {stats.get('memory_file', 'Unknown')}\n"
            
            role_counts = stats.get('messages_by_role', {})
            if role_counts:
                stats_text += "  • Messages by role:\n"
                for role, count in role_counts.items():
                    stats_text += f"    - {role}: {count}\n"
            
            issues = stats.get('issues', [])
            if issues:
                stats_text += f"  • Issues: {', '.join(issues)}\n"
            
            return stats_text
        except Exception as e:
            self.logger.error(f"Error getting memory stats: {e}")
            return f"❌ Error getting memory stats: {e}"

    # Extensibility hooks
    def detect_intent(self, user_input: str) -> Dict[str, Any]:
        """Stub for intent detection. Can be extended for MarketFlow integration.
        Args:
            user_input (str): The user's input text.
        Returns:
            Dict[str, Any]: Intent detection results.
        """
        # Basic intent detection for now
        intent = {"type": "general_query", "confidence": 1.0, "entities": []}
        
        # Check for special commands
        if user_input.lower().startswith('/'):
            if user_input.lower() == '/sources':
                intent = {"type": "show_sources", "confidence": 1.0, "entities": []}
            elif user_input.lower() == '/clear':
                intent = {"type": "clear_memory", "confidence": 1.0, "entities": []}
            elif user_input.lower() == '/repair':
                intent = {"type": "repair_memory", "confidence": 1.0, "entities": []}
            elif user_input.lower() == '/stats':
                intent = {"type": "memory_stats", "confidence": 1.0, "entities": []}
            elif user_input.lower() in ['/help', '/commands']:
                intent = {"type": "show_help", "confidence": 1.0, "entities": []}
        
        self.logger.debug(f"Intent detected: {intent}")
        return intent

    def integrate_marketflow_api(self, query: str) -> Dict[str, Any]:
        """Stub for MarketFlow API integration.
        Args:
            query (str): The user's query.
        Returns:
            Dict[str, Any]: MarketFlow API response data.
        """
        # Placeholder for future MarketFlow integration
        self.logger.debug(f"MarketFlow API integration called with query: {query}")
        return {"status": "not_implemented", "message": "MarketFlow API integration coming soon"}

    def show_help(self) -> str:
        """Show available commands and help."""
        help_text = """
🔮 Wyckoff & VPA RAG Q&A - Available Commands:

General Usage:
  • Ask any question about Wyckoff Method or Volume Price Analysis
  • Type 'quit' or 'exit' to end the session

Special Commands:
  • /sources  - Show sources from the last query
  • /clear    - Clear conversation memory  
  • /repair   - Repair conversation memory
  • /stats    - Show memory statistics
  • /help     - Show this help message

Examples:
  • "What are the phases of accumulation?"
  • "Explain volume analysis in trending markets"
  • "/sources" (after asking a question)
"""
        return help_text

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Wyckoff & VPA RAG Q&A - Interactive knowledge base assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python minimal_rag.py                                    # Use default session
  python minimal_rag.py --session user123                  # Use specific session
  python minimal_rag.py --model gpt-4 --session trader1   # Custom model and session
  python minimal_rag.py --system-prompt "You are expert"  # Custom system prompt
        """
    )
    
    parser.add_argument(
        '--session', '--session-id', '--user-id',
        default='default',
        help='Session or user ID for memory management (default: default)'
    )
    
    parser.add_argument(
        '--model',
        help='OpenAI model to use (if not specified, uses config default)'
    )
    
    parser.add_argument(
        '--system-prompt',
        help='Custom system prompt to initialize the conversation'
    )
    
    parser.add_argument(
        '--history-limit',
        type=int,
        default=5,
        help='Number of recent messages to include in context (default: 5)'
    )
    
    return parser.parse_args()

def main():
    """Main function with enhanced CLI support and error handling."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize RAG QA system
        try:
            rag_qa = MinimalRAGQA(
                model=args.model,
                session_id=args.session,
                system_prompt=args.system_prompt
            )
        except Exception as e:
            print(f"❌ Failed to initialize RAG QA system: {e}")
            return 1

        # Display welcome message
        print("🟢 Wyckoff & VPA RAG Q&A (Anna Coulling, etc)")
        print(f"📝 Session: {args.session}")
        print("Ask anything about Wyckoff, VPA, Anna Coulling's book.")
        print("Type 'quit' to exit, '/help' for commands.\n")
        
        rag_qa.logger.info(f"Started interactive RAG Q&A session for session: {args.session}")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                
                # Detect intent first
                intent = rag_qa.detect_intent(user_input)
                intent_type = intent.get('type', 'general_query')
                
                # Handle special commands
                if intent_type == 'show_sources':
                    print("\n" + rag_qa.display_sources())
                    continue
                elif intent_type == 'clear_memory':
                    print("\n" + rag_qa.clear_memory())
                    continue
                elif intent_type == 'repair_memory':
                    print("\n" + rag_qa.repair_memory())
                    continue
                elif intent_type == 'memory_stats':
                    print("\n" + rag_qa.get_memory_stats())
                    continue
                elif intent_type == 'show_help':
                    print(rag_qa.show_help())
                    continue
                
                # Handle exit commands
                if user_input.lower() in {"quit", "exit"}:
                    print("Goodbye!")
                    rag_qa.logger.info("User exited the session.")
                    break
                
                # Store user question in memory
                try:
                    rag_qa.memory_manager.add_message(role="user", content=user_input)
                    rag_qa.logger.info(f"Received user question: {user_input}")
                except Exception as e:
                    rag_qa.logger.error(f"Error storing user message: {e}")
                
                # Retrieve relevant chunks
                try:
                    top_chunks = chroma_retrieve_top_chunks(user_input, top_k=5)
                    rag_qa.logger.debug(f"Retrieved {len(top_chunks)} chunks")
                except Exception as e:
                    rag_qa.logger.error(f"Error retrieving chunks: {e}")
                    print("❌ Sorry, there was an error accessing the knowledge base.")
                    continue
                
                if not top_chunks:
                    response = "Sorry, I couldn't find anything relevant in the knowledge base."
                    print(f"\nAI: {response}")
                    rag_qa.logger.info(f"No relevant chunks found for question: {user_input}")
                    
                    # Still store the response in memory
                    try:
                        rag_qa.memory_manager.add_message(role="assistant", content=response)
                    except Exception as e:
                        rag_qa.logger.error(f"Error storing assistant response: {e}")
                    continue
                
                # Synthesize answer with LLM
                try:
                    answer = rag_qa.synthesize_with_openai(user_input, top_chunks)
                    print(f"\nAI: {answer}")
                    
                    # Store the answer in memory
                    try:
                        rag_qa.memory_manager.add_message(role="assistant", content=answer)
                        rag_qa.logger.info("Successfully stored assistant response in memory")
                    except Exception as e:
                        rag_qa.logger.error(f"Error storing assistant response: {e}")
                        
                except Exception as e:
                    rag_qa.logger.error(f"Error during LLM synthesis: {e}")
                    error_response = "Sorry, there was an error generating the answer."
                    print(f"\nAI: {error_response}")
                    
                    # Store error response in memory
                    try:
                        rag_qa.memory_manager.add_message(role="assistant", content=error_response)
                    except Exception as e:
                        rag_qa.logger.error(f"Error storing error response: {e}")
                        
            except KeyboardInterrupt:
                print("\nGoodbye!")
                rag_qa.logger.info("Session interrupted by user.")
                break
            except Exception as e:
                rag_qa.logger.error(f"Unexpected error in main loop: {e}")
                print(f"❌ An unexpected error occurred: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

