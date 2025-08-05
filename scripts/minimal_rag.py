# minimal_rag_qa.py

import os
import argparse
import openai
from typing import List, Optional

# Handle potential import issues gracefully
try:
    from rag.retriever import chroma_retrieve_top_chunks  # adjust import if needed
except ImportError as e:
    print(f"Warning: Could not import chroma_retrieve_top_chunks: {e}")
    print("You may need to install ChromaDB dependencies or ensure the knowledge base is set up.")
    
    def chroma_retrieve_top_chunks(query: str, top_k: int = 5):
        """Fallback function when ChromaDB is not available"""
        print(f"Mock retriever: Would search for '{query}' (top_k={top_k})")
        return [
            {
                "text": f"This is a mock response about {query}. ChromaDB is not available in this environment.",
                "metadata": {"source": "mock", "note": "ChromaDB not available"},
                "distance": 0.5,
                "embedding": []
            }
        ]

try:
    from marketflow.marketflow_config_manager import ConfigManager, create_app_config
except ImportError as e:
    print(f"Warning: Could not import config manager: {e}")
    def create_app_config(logger=None):
        return None

# Simple logger implementation to avoid import issues
import logging

def get_logger(module_name="MinimalRAG"):
    """Simple logger implementation"""
    logger = logging.getLogger(module_name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

# Simple memory manager implementation
class SimpleMemoryManager:
    """Simplified memory manager to avoid import issues"""
    
    def __init__(self, memory_file: str, max_memory_items: int = 50):
        import json
        import os
        
        self.memory_file = memory_file
        self.max_memory_items = max_memory_items
        self.memory = []
        self.system_messages = []
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(memory_file), exist_ok=True)
        
        # Load existing memory
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    content = f.read()
                    if content:
                        self.memory = json.loads(content)
            except Exception:
                self.memory = []
    
    def add_message(self, role: str, content: str, **kwargs):
        """Add a message to memory"""
        if role == "system":
            self.add_system_message(content)
            return
            
        message = {"role": role, "content": content}
        for key, value in kwargs.items():
            message[key] = value
            
        self.memory.append(message)
        self._trim_memory()
        self._save_memory()
    
    def add_system_message(self, content: str):
        """Add a system message"""
        self.system_messages.append({"role": "system", "content": content})
    
    def get_history(self, limit: int = None):
        """Get conversation history"""
        history = list(self.system_messages)
        if limit:
            recent_items = self.memory[-limit:] if self.memory else []
        else:
            recent_items = self.memory[-10:] if self.memory else []
        history.extend(recent_items)
        return history
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory = []
        self._save_memory()
    
    def clear_system_messages(self):
        """Clear system messages"""
        self.system_messages = []
    
    def clear_all(self):
        """Clear all memory"""
        self.clear_memory()
        self.clear_system_messages()
    
    def get_memory_stats(self):
        """Get memory statistics"""
        return {
            "total_messages": len(self.memory),
            "system_messages": len(self.system_messages),
            "memory_file": self.memory_file,
            "max_items": self.max_memory_items,
            "messages_by_role": {},
            "issues": []
        }
    
    def repair_conversation(self):
        """Repair conversation (simplified)"""
        return {
            "messages_before": len(self.memory),
            "messages_after": len(self.memory),
            "messages_removed": 0,
            "orphaned_tool_calls_before": 0,
            "orphaned_tool_calls_after": 0,
            "orphaned_tool_calls_fixed": 0
        }
    
    def _trim_memory(self):
        """Trim memory to max size"""
        if len(self.memory) > self.max_memory_items:
            self.memory = self.memory[-self.max_memory_items:]
    
    def _save_memory(self):
        """Save memory to file"""
        import json
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception:
            pass  # Ignore save errors for now

# Use the simplified memory manager
MemoryManager = SimpleMemoryManager

class MinimalRAGQA:
    def __init__(self, model: str = None, session_id: str = "default", 
                 system_prompt: str = None, memory_limit: int = 50) -> None:
        """Initialize the MinimalRAGQA class.
        
        Args:
            model (str): The OpenAI model to use for synthesis.
            session_id (str): Session identifier for memory management.
            system_prompt (str): Custom system prompt to initialize conversation.
            memory_limit (int): Maximum number of messages to keep in memory.
        """
        # Initialize logger
        self.logger = get_logger("MinimalRAGQA")
        
        # Store session info
        self.session_id = session_id
        
        # Initialize configuration manager
        try:
            self.config_manager = create_app_config(logger=self.logger)
            self.logger.info("Configuration manager initialized.")
        except Exception as e:
            self.logger.error(f"Failed to initialize config manager: {e}")
            self.config_manager = None
            
        self.model = model or (self.config_manager.get_llm_model() if self.config_manager else "gpt-3.5-turbo")
        if not self.model:
            raise ValueError("No LLM model configured.")
            
        # Log the initialization
        self.logger.info(f"Initialized MinimalRAGQA with model: {self.model}, session: {session_id}")

        # Create session-specific memory file path
        memory_file = f".marketflow/memory/session_{session_id}.json"
        
        # Initialize memory manager with error handling
        try:
            self.memory_manager = MemoryManager(memory_file=memory_file, max_memory_items=memory_limit)
            self.logger.info(f"Memory manager initialized with file: {memory_file}")
        except Exception as e:
            self.logger.error(f"Failed to initialize memory manager: {e}")
            raise
            
        # Initialize with system prompt if provided
        if system_prompt:
            self.set_system_prompt(system_prompt)
        else:
            # Default system prompt
            default_prompt = (
                "You are an assistant specializing in Wyckoff Method and Anna Coulling's Volume Price Analysis (VPA). "
                "You provide clear, educational explanations about market analysis, trading principles, and technical analysis. "
                "Always cite sources when possible and encourage proper risk management."
            )
            self.set_system_prompt(default_prompt)
            
        # Store last retrieved sources for /sources command
        self.last_sources = []

    def set_system_prompt(self, system_prompt: str) -> None:
        """Set the system prompt for the conversation."""
        try:
            self.memory_manager.clear_system_messages()  # Clear existing system messages
            self.memory_manager.add_system_message(system_prompt)
            self.logger.info("System prompt set successfully")
        except Exception as e:
            self.logger.error(f"Failed to set system prompt: {e}")
            
    def get_memory_stats(self) -> dict:
        """Get memory statistics."""
        try:
            return self.memory_manager.get_memory_stats()
        except Exception as e:
            self.logger.error(f"Failed to get memory stats: {e}")
            return {}
            
    def clear_memory(self) -> None:
        """Clear conversation memory."""
        try:
            self.memory_manager.clear_memory()
            self.logger.info("Memory cleared successfully")
        except Exception as e:
            self.logger.error(f"Failed to clear memory: {e}")
            
    def repair_memory(self) -> dict:
        """Repair conversation memory."""
        try:
            return self.memory_manager.repair_conversation()
        except Exception as e:
            self.logger.error(f"Failed to repair memory: {e}")
            return {}
            
    def get_conversation_history(self, limit: int = 10) -> List[dict]:
        """Get conversation history with optional limit."""
        try:
            return self.memory_manager.get_history(limit=limit)
        except Exception as e:
            self.logger.error(f"Failed to get history: {e}")
            return []

    def get_recent_history(self, n=5):
        """Get the last n messages from memory and concatenate them for context.
        Args:
            n (int): Number of recent messages to retrieve.
        Returns:
            str: Concatenated string of the last n messages.
        """
        history = self.memory_manager.get_history(limit=n)
        self.logger.debug(f"Recent history: {history}")
        return "\n".join(f"{msg['role']}: {msg['content']}" for msg in history if msg.get('role') != 'system')

    def synthesize_with_openai(self, question: str, chunks: List[dict]) -> str:
        """Synthesizes an answer using OpenAI's LLM based on the provided question and context chunks.
        Args:
            question (str): The user's question.
            chunks (List[dict]): List of context chunks retrieved from the knowledge base.
        Returns:
            str: The synthesized answer from the LLM.
        """
        try:
            recent_history = self.get_recent_history(n=5)
            self.logger.debug(f"Recent history for context:\n{recent_history}")
            self.logger.info(f"Synthesizing answer with OpenAI for question: {question}")
            
            # Store sources for /sources command
            self.last_sources = []
            
            # Build context with metadata
            context_parts = []
            for i, chunk in enumerate(chunks, 1):
                text = chunk.get("text", "")
                metadata = chunk.get("metadata", {})
                distance = chunk.get("distance", 0.0)
                
                # Store source info
                source_info = {
                    "index": i,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "metadata": metadata,
                    "relevance_score": f"{1.0 - distance:.3f}" if distance else "N/A"
                }
                self.last_sources.append(source_info)
                
                # Format context with metadata
                metadata_str = ""
                if metadata:
                    metadata_items = []
                    for key, value in metadata.items():
                        if value:  # Only include non-empty metadata
                            metadata_items.append(f"{key}: {value}")
                    if metadata_items:
                        metadata_str = f" [Source: {', '.join(metadata_items)}]"
                
                context_parts.append(f"Context {i}{metadata_str}:\n{text}")
            
            context = "\n\n".join(context_parts)
            self.logger.debug(f"Context for synthesis:\n{context[:500]}...")

            # Build comprehensive prompt
            prompt_parts = []
            
            # Add conversation history for context
            if recent_history:
                prompt_parts.append(f"Previous conversation context:\n{recent_history}\n")
            
            # Add main context and question
            prompt_parts.extend([
                f"Given this information from the knowledge base:\n---\n{context}\n---\n",
                f"**Question:** {question}\n",
                "Provide a clear, concise answer based on the provided context. If you reference specific information, ",
                "try to indicate which source it comes from when relevant."
            ])
            
            prompt = "".join(prompt_parts)
            
            self.logger.debug(f"Prompt sent to OpenAI (first 500 chars):\n{prompt[:500]}...")
            
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
            return answer
            
        except AttributeError:
            # For openai==0.x
            try:
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
            except Exception as e:
                self.logger.error(f"Error with OpenAI 0.x API: {e}")
                raise
        except Exception as e:
            self.logger.error(f"Error during synthesis: {e}")
            raise

    def display_sources(self) -> None:
        """Display sources from the last query."""
        if not self.last_sources:
            print("\n📚 No sources available from recent queries.")
            return
            
        print(f"\n📚 Sources from last query ({len(self.last_sources)} found):")
        print("-" * 60)
        
        for source in self.last_sources:
            print(f"[{source['index']}] Relevance: {source['relevance_score']}")
            if source['metadata']:
                for key, value in source['metadata'].items():
                    if value:
                        print(f"    {key}: {value}")
            print(f"    Preview: {source['text_preview']}")
            print()

    def detect_intent(self, user_input: str) -> dict:
        """Detect user intent and extract relevant information.
        
        This is an extensibility hook for future MarketFlow integration.
        Currently handles basic CLI commands.
        
        Args:
            user_input (str): User input to analyze
            
        Returns:
            dict: Intent detection results
        """
        user_input = user_input.strip()
        
        # Handle CLI commands
        if user_input.startswith('/'):
            command = user_input.lower()
            
            if command in ['/sources', '/source']:
                return {"type": "command", "command": "sources"}
            elif command in ['/clear', '/reset']:
                return {"type": "command", "command": "clear"}
            elif command in ['/repair', '/fix']:
                return {"type": "command", "command": "repair"}
            elif command.startswith('/history'):
                # Extract number if provided: /history 20
                parts = command.split()
                limit = 10  # default
                if len(parts) > 1:
                    try:
                        limit = int(parts[1])
                    except ValueError:
                        pass
                return {"type": "command", "command": "history", "limit": limit}
            elif command in ['/stats', '/status']:
                return {"type": "command", "command": "stats"}
            elif command in ['/help', '/?']:
                return {"type": "command", "command": "help"}
            else:
                return {"type": "command", "command": "unknown", "original": user_input}
        
        # Future: Add more sophisticated intent detection here
        # - Market data queries
        # - Analysis requests
        # - Trading strategy questions
        # - Technical analysis requests
        
        return {"type": "question", "original": user_input}

    def handle_command(self, intent: dict) -> bool:
        """Handle CLI commands.
        
        Args:
            intent (dict): Intent detection results
            
        Returns:
            bool: True if command was handled, False if processing should continue
        """
        command = intent.get("command")
        
        if command == "sources":
            self.display_sources()
            return True
            
        elif command == "clear":
            self.clear_memory()
            print("\n🗑️  Memory cleared successfully.")
            return True
            
        elif command == "repair":
            stats = self.repair_memory()
            print(f"\n🔧 Memory repair completed:")
            print(f"   Messages before: {stats.get('messages_before', 0)}")
            print(f"   Messages after: {stats.get('messages_after', 0)}")
            print(f"   Orphaned tool calls fixed: {stats.get('orphaned_tool_calls_fixed', 0)}")
            return True
            
        elif command == "history":
            limit = intent.get("limit", 10)
            history = self.get_conversation_history(limit=limit)
            print(f"\n📖 Last {len(history)} messages:")
            print("-" * 60)
            for msg in history:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                if role != 'system':  # Skip system messages in history display
                    print(f"{role.upper()}: {content}")
                    print()
            return True
            
        elif command == "stats":
            stats = self.get_memory_stats()
            print("\n📊 Memory Statistics:")
            print("-" * 30)
            print(f"Total messages: {stats.get('total_messages', 0)}")
            print(f"System messages: {stats.get('system_messages', 0)}")
            print(f"Memory file: {stats.get('memory_file', 'N/A')}")
            print(f"Max items: {stats.get('max_items', 0)}")
            
            role_counts = stats.get('messages_by_role', {})
            if role_counts:
                print("\nMessages by role:")
                for role, count in role_counts.items():
                    print(f"  {role}: {count}")
                    
            issues = stats.get('issues', [])
            if issues:
                print("\nIssues detected:")
                for issue in issues:
                    print(f"  ⚠️  {issue}")
            return True
            
        elif command == "help":
            self.display_help()
            return True
            
        elif command == "unknown":
            print(f"\n❓ Unknown command: {intent.get('original')}")
            print("Type '/help' for available commands.")
            return True
            
        return False

    def display_help(self) -> None:
        """Display help information."""
        print("\n🤖 Wyckoff & VPA RAG Q&A - Available Commands:")
        print("-" * 50)
        print("/sources     - Show sources from last query")
        print("/clear       - Clear conversation memory")
        print("/repair      - Repair memory inconsistencies")  
        print("/history [N] - Show last N messages (default: 10)")
        print("/stats       - Show memory statistics")
        print("/help        - Show this help message")
        print("quit/exit    - Exit the application")
        print("\nAsk any question about Wyckoff Method, VPA, or trading analysis!")

    def marketflow_api_hook(self, user_input: str, intent: dict) -> Optional[dict]:
        """Hook for future MarketFlow API integration.
        
        This method provides an extension point for integrating with MarketFlow
        analysis capabilities, market data, and trading signals.
        
        Args:
            user_input (str): Original user input
            intent (dict): Detected intent information
            
        Returns:
            Optional[dict]: MarketFlow analysis results or None
        """
        # Future implementation could include:
        # - Market data queries
        # - Technical analysis requests
        # - Pattern recognition
        # - Signal generation
        # - Portfolio analysis
        
        self.logger.debug(f"MarketFlow API hook called with intent: {intent}")
        return None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MinimalRAG QA - Wyckoff & VPA Question Answering System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python minimal_rag.py --session myanalysis --system-prompt "You are a trading expert"
  python minimal_rag.py --model gpt-4 --memory-limit 100
  python minimal_rag.py --session backtesting --help-commands

Available in-chat commands:
  /sources     - Show sources from last query
  /clear       - Clear conversation memory  
  /repair      - Repair memory inconsistencies
  /history [N] - Show last N messages
  /stats       - Show memory statistics
  /help        - Show help message
        """
    )
    
    parser.add_argument(
        '--session', '--session-id',
        default='default',
        help='Session ID for memory management (default: default)'
    )
    
    parser.add_argument(
        '--model',
        help='OpenAI model to use (default: from config or gpt-3.5-turbo)'
    )
    
    parser.add_argument(
        '--system-prompt',
        help='Custom system prompt to initialize conversation'
    )
    
    parser.add_argument(
        '--memory-limit',
        type=int,
        default=50,
        help='Maximum number of messages to keep in memory (default: 50)'
    )
    
    parser.add_argument(
        '--help-commands',
        action='store_true',
        help='Show available in-chat commands and exit'
    )
    
    return parser.parse_args()

def main():
    """Main function with enhanced argument parsing and error handling."""
    args = parse_arguments()
    
    if args.help_commands:
        print("🤖 Wyckoff & VPA RAG Q&A - Available Commands:")
        print("-" * 50)
        print("/sources     - Show sources from last query")
        print("/clear       - Clear conversation memory")
        print("/repair      - Repair memory inconsistencies")  
        print("/history [N] - Show last N messages (default: 10)")
        print("/stats       - Show memory statistics")
        print("/help        - Show this help message")
        print("quit/exit    - Exit the application")
        print("\nAsk any question about Wyckoff Method, VPA, or trading analysis!")
        return
    
    try:
        # Initialize RAG QA system
        rag_qa = MinimalRAGQA(
            model=args.model,
            session_id=args.session,
            system_prompt=args.system_prompt,
            memory_limit=args.memory_limit
        )
        
        # Display startup information
        print("🟢 Wyckoff & VPA RAG Q&A (Anna Coulling, etc)")
        print(f"Session: {args.session} | Model: {rag_qa.model}")
        print("Ask anything about Wyckoff, VPA, Anna Coulling's book.")
        print("Type '/help' for commands or 'quit' to exit.\n")
        
        rag_qa.logger.info(f"Started interactive RAG Q&A session with session: {args.session}")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                # Check for exit commands
                if user_input.lower() in {"quit", "exit"}:
                    print("Goodbye!")
                    rag_qa.logger.info("User exited the session.")
                    break
                
                # Detect intent and handle commands
                intent = rag_qa.detect_intent(user_input)
                
                if intent["type"] == "command":
                    if rag_qa.handle_command(intent):
                        continue  # Command was handled, get next input
                
                # Store user question in memory
                rag_qa.memory_manager.add_message(role="user", content=user_input)
                rag_qa.logger.info(f"Received user question: {user_input}")
                
                # Check for MarketFlow API integration
                marketflow_result = rag_qa.marketflow_api_hook(user_input, intent)
                if marketflow_result:
                    # Future: Handle MarketFlow-specific responses
                    rag_qa.logger.info("MarketFlow API integration returned results")
                
                # Retrieve top chunks from knowledge base
                try:
                    top_chunks = chroma_retrieve_top_chunks(user_input, top_k=5)
                    rag_qa.logger.debug(f"Retrieved {len(top_chunks)} chunks from knowledge base")
                except Exception as e:
                    rag_qa.logger.error(f"Error retrieving chunks: {e}")
                    top_chunks = []
                
                if not top_chunks:
                    response = "Sorry, I couldn't find anything relevant in the knowledge base for your question."
                    print(f"\nAI: {response}")
                    rag_qa.memory_manager.add_message(role="assistant", content=response)
                    rag_qa.logger.info("No relevant chunks found for question")
                    continue
                
                # Synthesize answer with LLM
                try:
                    answer = rag_qa.synthesize_with_openai(user_input, top_chunks)
                    rag_qa.logger.info("Successfully synthesized answer")
                    
                    # Store the answer in memory
                    rag_qa.memory_manager.add_message(role="assistant", content=answer)
                    
                    print(f"\nAI: {answer}")
                    
                except Exception as e:
                    rag_qa.logger.error(f"Error during LLM synthesis: {e}")
                    error_response = "Sorry, there was an error generating the answer. Please try again."
                    print(f"\nAI: {error_response}")
                    rag_qa.memory_manager.add_message(role="assistant", content=error_response)
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                rag_qa.logger.info("Session interrupted by user")
                break
            except Exception as e:
                rag_qa.logger.error(f"Unexpected error in main loop: {e}")
                print(f"\n❌ An unexpected error occurred: {e}")
                print("Please try again or type 'quit' to exit.")
                
    except Exception as e:
        print(f"❌ Failed to initialize RAG QA system: {e}")
        print("Please check your configuration and try again.")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code or 0)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        exit(1)

