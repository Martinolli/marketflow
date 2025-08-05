"""
Enhanced Minimal RAG QA Script

A foundational RAG Q&A system for Wyckoff & VPA with comprehensive session management,
improved prompt engineering, and extensibility hooks for MarketFlow integration.

Features:
- Session/user management with dynamic memory files
- Enhanced MemoryManager integration (system messages, repair, history limits)
- RAG chunk metadata display with source information
- Customizable system prompts and improved context threading
- Comprehensive error handling and logging
- Extensibility hooks for intent detection and MarketFlow API integration
"""

import sys
import os
import argparse  
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import openai
except ImportError:
    print("❌ OpenAI not available. Please install: pip install openai")
    sys.exit(1)

# Import components directly to avoid package init issues
try:
    from marketflow.marketflow_memory_manager import MemoryManager
    from marketflow.marketflow_logger import get_logger
    from marketflow.marketflow_config_manager import create_app_config
except ImportError as e:
    print(f"❌ Cannot import MarketFlow components: {e}")
    print("Please ensure you're running from the repository root directory.")
    sys.exit(1)

# Try to import RAG retriever, but make it optional for now
try:
    from rag.retriever import chroma_retrieve_top_chunks
    RAG_AVAILABLE = True
except ImportError:
    print("⚠️  RAG retriever not available. Running in limited mode.")
    RAG_AVAILABLE = False
    
    def chroma_retrieve_top_chunks(query: str, top_k: int = 5):
        """Placeholder retriever when RAG is not available."""
        return [
            {
                "text": f"This is a placeholder response for query: {query}",
                "metadata": {"source": "placeholder", "page": "1"},
                "distance": 0.5
            }
        ]

class MinimalRAGQA:
    """Enhanced RAG Q&A system with session management and extensibility."""
    
    def __init__(self, model: Optional[str] = None, session_id: str = "default", 
                 system_prompt: Optional[str] = None, memory_dir: Optional[str] = None) -> None:
        """Initialize the MinimalRAGQA class.
        
        Args:
            model (str, optional): The OpenAI model to use for synthesis.
            session_id (str): Session identifier for memory management.
            system_prompt (str, optional): Custom system prompt.
            memory_dir (str, optional): Directory for memory files.
        """
        # Initialize logging
        self.logger = get_logger("MinimalRAGQA")
        self.session_id = session_id
        
        # Initialize configuration manager
        try:
            self.config_manager = create_app_config(logger=self.logger)
            self.logger.info("Configuration manager initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize configuration manager: {e}")
            raise
            
        # Initialize model
        self.model = model or self.config_manager.get_llm_model()
        if not self.model:
            raise ValueError("No LLM model configured. Please set model parameter or configure in config.")
        self.logger.info(f"Initialized MinimalRAGQA with model: {self.model}")
        
        # Setup memory management
        if memory_dir is None:
            memory_dir = ".marketflow/memory"
        
        # Ensure memory directory exists
        Path(memory_dir).mkdir(parents=True, exist_ok=True)
        
        # Create session-specific memory file
        memory_file = f"{memory_dir}/session_{session_id}.json"
        
        try:
            self.memory_manager = MemoryManager(memory_file=memory_file)
            self.logger.info(f"Memory manager initialized with file: {memory_file}")
        except Exception as e:
            self.logger.error(f"Failed to initialize memory manager: {e}")
            raise
            
        # Initialize system prompt
        self.default_system_prompt = (
            "You are an expert assistant specializing in Wyckoff methodology and "
            "Anna Coulling's Volume Price Analysis (VPA). You provide clear, accurate, "
            "and actionable insights based on the provided context. When referencing "
            "sources, mention them clearly."
        )
        
        if system_prompt:
            self.memory_manager.add_system_message(system_prompt)
            self.logger.info("Custom system prompt added to memory.")
        else:
            self.memory_manager.add_system_message(self.default_system_prompt)
            self.logger.info("Default system prompt added to memory.")
            
        # Initialize extensibility hooks
        self.intent_detection_enabled = False
        self.marketflow_integration_enabled = False

    def get_recent_history(self, n: int = 5) -> str:
        """Get the last n messages from memory and format them for context.
        
        Args:
            n (int): Number of recent messages to retrieve.
            
        Returns:
            str: Formatted string of the last n messages.
        """
        try:
            # Use MemoryManager's get_history with limit
            history = self.memory_manager.get_history(limit=n)
            self.logger.debug(f"Retrieved {len(history)} messages from history.")
            
            # Filter out system messages for context (they're handled separately)
            conversation_history = [msg for msg in history if msg.get('role') != 'system']
            
            if not conversation_history:
                return ""
                
            formatted_history = []
            for msg in conversation_history[-n:]:  # Get last n messages
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                formatted_history.append(f"{role.capitalize()}: {content}")
                
            result = "\n".join(formatted_history)
            self.logger.debug(f"Formatted history: {result[:200]}...")
            return result
            
        except Exception as e:
            self.logger.error(f"Error retrieving recent history: {e}")
            return ""

    def format_chunks_with_metadata(self, chunks: List[Dict[str, Any]]) -> str:
        """Format chunks with metadata for better context.
        
        Args:
            chunks (List[Dict]): List of context chunks with metadata.
            
        Returns:
            str: Formatted context string with metadata.
        """
        if not chunks:
            return ""
            
        formatted_parts = []
        for i, chunk in enumerate(chunks, 1):
            text = chunk.get("text", "")
            metadata = chunk.get("metadata", {})
            
            # Extract metadata information
            source = metadata.get("source", "Unknown")
            page = metadata.get("page", "Unknown")
            
            # Format chunk with metadata
            chunk_header = f"[Source {i}: {source}, Page: {page}]"
            formatted_parts.append(f"{chunk_header}\n{text}")
            
        return "\n\n".join(formatted_parts)

    def synthesize_with_openai(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        """Synthesizes an answer using OpenAI's LLM with enhanced context and metadata.
        
        Args:
            question (str): The user's question.
            chunks (List[Dict]): List of context chunks retrieved from the knowledge base.
            
        Returns:
            str: The synthesized answer from the LLM.
        """
        try:
            # Get recent conversation history for context
            recent_history = self.get_recent_history(n=5)
            self.logger.debug(f"Recent history for context (length: {len(recent_history)})")
            
            # Format chunks with metadata
            context_with_metadata = self.format_chunks_with_metadata(chunks)
            self.logger.debug(f"Context with metadata prepared (length: {len(context_with_metadata)})")
            
            # Build enhanced prompt with proper context threading
            prompt_parts = []
            
            if recent_history:
                prompt_parts.append(f"Recent conversation context:\n{recent_history}")
                
            if context_with_metadata:
                prompt_parts.append(f"Relevant information from knowledge base:\n---\n{context_with_metadata}\n---")
            else:
                self.logger.warning("No context chunks provided for synthesis")
                
            prompt_parts.append(f"Question: {question}")
            prompt_parts.append(
                "Please provide a clear, concise answer based on the above information. "
                "If you reference specific sources, mention them in your response."
            )
            
            full_prompt = "\n\n".join(prompt_parts)
            
            self.logger.debug(f"Sending prompt to OpenAI (length: {len(full_prompt)})")
            self.logger.debug(f"Prompt preview: {full_prompt[:500]}...")
            
            # Call OpenAI API
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            
            answer = response.choices[0].message.content.strip()
            self.logger.info("Successfully received answer from OpenAI.")
            self.logger.debug(f"Answer preview: {answer[:200]}...")
            
            return answer
            
        except Exception as e:
            self.logger.error(f"Error during LLM synthesis: {e}")
            raise

    def display_sources(self, chunks: List[Dict[str, Any]]) -> None:
        """Display source information for retrieved chunks.
        
        Args:
            chunks (List[Dict]): List of context chunks with metadata.
        """
        if not chunks:
            print("No sources available.")
            return
            
        print("\n📚 Sources:")
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "Unknown")
            page = metadata.get("page", "Unknown")
            distance = chunk.get("distance", "N/A")
            score = chunk.get("score", "N/A")
            
            relevance = f"Distance: {distance}" if distance != "N/A" else f"Score: {score}"
            print(f"{i}. {source} (Page: {page}) - {relevance}")
            
    def clear_memory(self) -> None:
        """Clear conversation memory but keep system messages."""
        try:
            self.memory_manager.clear_memory()
            self.logger.info(f"Cleared memory for session: {self.session_id}")
            print(f"✅ Memory cleared for session '{self.session_id}'")
        except Exception as e:
            self.logger.error(f"Error clearing memory: {e}")
            print(f"❌ Error clearing memory: {e}")
            
    def repair_memory(self) -> None:
        """Repair conversation memory by fixing any issues."""
        try:
            repair_stats = self.memory_manager.repair_conversation()
            self.logger.info(f"Memory repair completed: {repair_stats}")
            print(f"🔧 Memory repair completed:")
            print(f"   Messages before: {repair_stats['messages_before']}")
            print(f"   Messages after: {repair_stats['messages_after']}")
            print(f"   Issues fixed: {repair_stats['orphaned_tool_calls_fixed']}")
        except Exception as e:
            self.logger.error(f"Error repairing memory: {e}")
            print(f"❌ Error repairing memory: {e}")
            
    def get_memory_stats(self) -> None:
        """Display memory statistics."""
        try:
            stats = self.memory_manager.get_memory_stats()
            print(f"\n📊 Memory Statistics for session '{self.session_id}':")
            print(f"   Total messages: {stats['total_messages']}")
            print(f"   System messages: {stats['system_messages']}")
            print(f"   Memory file: {stats['memory_file']}")
            
            if stats.get('messages_by_role'):
                print("   Messages by role:")
                for role, count in stats['messages_by_role'].items():
                    print(f"     {role}: {count}")
                    
            if stats.get('issues'):
                print("   Issues found:")
                for issue in stats['issues']:
                    print(f"     ⚠️  {issue}")
                    
        except Exception as e:
            self.logger.error(f"Error getting memory stats: {e}")
            print(f"❌ Error getting memory stats: {e}")

    # Extensibility hooks
    def detect_intent(self, user_input: str) -> Optional[str]:
        """Detect user intent for advanced routing (extensibility hook).
        
        Args:
            user_input (str): User's input text.
            
        Returns:
            Optional[str]: Detected intent or None.
        """
        if not self.intent_detection_enabled:
            return None
            
        # TODO: Implement intent detection logic
        # This is a placeholder for future MarketFlow integration
        self.logger.debug(f"Intent detection placeholder for: {user_input}")
        return None
        
    def call_marketflow_api(self, intent: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call MarketFlow API based on detected intent (extensibility hook).
        
        Args:
            intent (str): Detected user intent.
            parameters (Dict): Parameters for the API call.
            
        Returns:
            Optional[Dict]: API response or None.
        """
        if not self.marketflow_integration_enabled:
            return None
            
        # TODO: Implement MarketFlow API integration
        # This is a placeholder for future integration
        self.logger.debug(f"MarketFlow API call placeholder - Intent: {intent}, Params: {parameters}")
        return None
def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Enhanced Minimal RAG Q&A for Wyckoff & VPA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands during conversation:
  /sources    - Show sources for the last answer
  /clear      - Clear conversation memory
  /repair     - Repair conversation memory
  /stats      - Show memory statistics
  /help       - Show this help
  quit/exit   - Exit the program
        """
    )
    
    parser.add_argument(
        "--session-id", "--session", "-s",
        type=str,
        default="default",
        help="Session ID for memory management (default: 'default')"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        help="OpenAI model to use (overrides config)"
    )
    
    parser.add_argument(
        "--system-prompt",
        type=str,
        help="Custom system prompt"
    )
    
    parser.add_argument(
        "--memory-dir",
        type=str,
        help="Directory for memory files (default: .marketflow/memory)"
    )
    
    parser.add_argument(
        "--history-limit",
        type=int,
        default=5,
        help="Number of recent messages to include in context (default: 5)"
    )
    
    parser.add_argument(
        "--enable-intent-detection",
        action="store_true",
        help="Enable intent detection (experimental)"
    )
    
    parser.add_argument(
        "--enable-marketflow-integration",
        action="store_true", 
        help="Enable MarketFlow API integration (experimental)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level (default: INFO)"
    )
    
    return parser.parse_args()


def handle_command(command: str, rag_qa: MinimalRAGQA, last_chunks: List[Dict[str, Any]]) -> bool:
    """Handle special commands during conversation.
    
    Args:
        command (str): The command to handle.
        rag_qa (MinimalRAGQA): The RAG QA instance.
        last_chunks (List[Dict]): Last retrieved chunks for source display.
        
    Returns:
        bool: True if the command was handled, False otherwise.
    """
    command = command.lower().strip()
    
    if command == "/sources":
        rag_qa.display_sources(last_chunks)
        return True
    elif command == "/clear":
        rag_qa.clear_memory()
        return True
    elif command == "/repair":
        rag_qa.repair_memory()
        return True
    elif command == "/stats":
        rag_qa.get_memory_stats()
        return True
    elif command == "/help":
        print("""
Available commands:
  /sources  - Show sources for the last answer
  /clear    - Clear conversation memory
  /repair   - Repair conversation memory  
  /stats    - Show memory statistics
  /help     - Show this help
  quit/exit - Exit the program
        """)
        return True
        
    return False


def main():
    """Enhanced main function with comprehensive session management."""
    args = parse_arguments()
    
    # Setup logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    try:
        # Initialize RAG QA system with session management
        rag_qa = MinimalRAGQA(
            model=args.model,
            session_id=args.session_id,
            system_prompt=args.system_prompt,
            memory_dir=args.memory_dir
        )
        
        # Enable experimental features if requested
        rag_qa.intent_detection_enabled = args.enable_intent_detection
        rag_qa.marketflow_integration_enabled = args.enable_marketflow_integration
        
        if args.enable_intent_detection:
            print("🧠 Intent detection enabled (experimental)")
        if args.enable_marketflow_integration:
            print("🔌 MarketFlow integration enabled (experimental)")
            
    except Exception as e:
        print(f"❌ Failed to initialize RAG QA system: {e}")
        sys.exit(1)

    # Display startup information
    print("🟢 Enhanced Wyckoff & VPA RAG Q&A System")
    print("=" * 50)
    print(f"Session ID: {args.session_id}")
    print(f"Model: {rag_qa.model}")
    print(f"History limit: {args.history_limit}")
    print("\nAsk anything about Wyckoff, VPA, or Anna Coulling's methods.")
    print("Type '/help' for commands or 'quit' to exit.\n")
    
    rag_qa.logger.info(f"Started enhanced RAG Q&A session: {args.session_id}")
    
    last_retrieved_chunks = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            # Handle exit commands
            if user_input.lower() in {"quit", "exit"}:
                print("👋 Goodbye!")
                rag_qa.logger.info("User exited the session.")
                break
                
            # Handle special commands
            if user_input.startswith("/"):
                if handle_command(user_input, rag_qa, last_retrieved_chunks):
                    continue
                else:
                    print(f"❌ Unknown command: {user_input}. Type '/help' for available commands.")
                    continue
            
            # Store user question in memory
            rag_qa.memory_manager.add_message(role="user", content=user_input)
            rag_qa.logger.info(f"Received user question: {user_input}")
            
            # Check for intent detection (extensibility hook)
            intent = rag_qa.detect_intent(user_input)
            if intent:
                rag_qa.logger.info(f"Detected intent: {intent}")
                # TODO: Handle intent-based routing
                
            # Retrieve relevant chunks
            try:
                top_chunks = chroma_retrieve_top_chunks(user_input, top_k=5)
                last_retrieved_chunks = top_chunks  # Store for /sources command
                rag_qa.logger.debug(f"Retrieved {len(top_chunks)} chunks")
                
                if not top_chunks:
                    print("AI: Sorry, I couldn't find anything relevant in the knowledge base.")
                    rag_qa.logger.info(f"No relevant chunks found for question: {user_input}")
                    continue
                    
            except Exception as e:
                rag_qa.logger.error(f"Error retrieving chunks: {e}")
                print("AI: Sorry, there was an error searching the knowledge base.")
                continue
            
            # Synthesize answer with LLM
            try:
                answer = rag_qa.synthesize_with_openai(user_input, top_chunks)
                
                # Store the answer in memory
                rag_qa.memory_manager.add_message(role="assistant", content=answer)
                rag_qa.logger.info("Answer synthesized and stored in memory.")
                
                print(f"\nAI: {answer}")
                print(f"\n💡 Tip: Type '/sources' to see source information for this answer.")
                
            except Exception as e:
                rag_qa.logger.error(f"Error during LLM synthesis: {e}")
                print("AI: Sorry, there was an error generating the answer. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            rag_qa.logger.info("Session interrupted by user.")
            break
        except Exception as e:
            rag_qa.logger.error(f"Unexpected error in main loop: {e}")
            print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

