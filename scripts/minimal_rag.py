# minimal_rag_qa.py

import openai
import argparse
import os
import sys
import tempfile
from typing import List, Optional
from pathlib import Path

# Add the parent directory to sys.path to import modules  
sys.path.append(str(Path(__file__).parent.parent))

try:
    from rag.retriever import chroma_retrieve_top_chunks
except ImportError as e:
    print(f"Warning: Could not import retriever: {e}")
    # Create a stub function for testing
    def chroma_retrieve_top_chunks(query, top_k=5):
        return []

# Import specific modules directly to avoid __init__.py dependencies
try:
    sys.path.append(str(Path(__file__).parent.parent / "marketflow"))
    from marketflow_logger import get_logger
    from marketflow_memory_manager import MemoryManager
    from marketflow_config_manager import ConfigManager, create_app_config
except ImportError as e:
    print(f"Warning: Could not import some marketflow modules: {e}")
    
    # Create stubs for testing
    def get_logger(name):
        import logging
        return logging.getLogger(name)
    
    class StubMemoryManager:
        def __init__(self, memory_file=None, **kwargs):
            self.memory_file = memory_file or tempfile.mktemp(suffix='.json')
            self.memory = []
            self.system_messages = []
            
        def add_message(self, role, content, **kwargs):
            self.memory.append({"role": role, "content": content})
            
        def add_system_message(self, content):
            self.system_messages.append({"role": "system", "content": content})
            
        def get_history(self, limit=None):
            history = list(self.system_messages)
            if limit:
                history.extend(self.memory[-limit:])
            else:
                history.extend(self.memory)
            return history
            
        def clear_memory(self):
            self.memory = []
            
        def repair_conversation(self):
            return {"messages_before": len(self.memory), "messages_after": len(self.memory), 
                   "messages_removed": 0, "orphaned_tool_calls_fixed": 0}
                   
        def get_memory_stats(self):
            return {"total_messages": len(self.memory), "system_messages": len(self.system_messages),
                   "max_items": 100, "messages_by_role": {}, "issues": []}
    
    MemoryManager = StubMemoryManager
    
    class StubConfigManager:
        def get_llm_model(self):
            return "gpt-3.5-turbo"
    
    def create_app_config(logger=None):
        return StubConfigManager()

class MinimalRAGQA:
    def __init__(self, model: Optional[str] = None, session_id: str = "default", 
                 system_prompt: Optional[str] = None) -> None:
        """Initialize the MinimalRAGQA class.
        Args:
            model (str): The OpenAI model to use for synthesis.
            session_id (str): Session identifier for memory management.
            system_prompt (str): Custom system prompt to initialize the session.
        """
        # Initialize logger
        self.logger = get_logger("MinimalRAGQA")
        
        # Initialize configuration manager
        self.config_manager = create_app_config(logger=self.logger)
        self.logger.info("Configuration manager initialized.")
        
        # Set model
        self.model = model or self.config_manager.get_llm_model()
        if not self.model:
            raise ValueError("No LLM model configured.")
        
        # Initialize session-specific memory
        self.session_id = session_id
        memory_file = f".marketflow/memory/session_{session_id}.json"
        self.memory_manager = MemoryManager(memory_file=memory_file)
        
        # Add system prompt if provided
        self.system_prompt = system_prompt or (
            "You are an assistant specializing in Wyckoff and Anna Coulling's VPA (Volume Price Analysis). "
            "Provide clear, concise answers based on the provided context and conversation history."
        )
        
        # Initialize system message if not already present
        if not self.memory_manager.system_messages:
            self.memory_manager.add_system_message(self.system_prompt)
        
        self.logger.info(f"Initialized MinimalRAGQA with model: {self.model}, session: {session_id}")
        self.logger.info(f"Memory manager initialized with file: {memory_file}")

    def get_recent_history(self, n=5):
        """Get the last n messages from memory and concatenate them for context.
        Args:
            n (int): Number of recent messages to retrieve.
        Returns:
            str: Concatenated string of the last n messages.
        """
        history = self.memory_manager.get_history(limit=n)
        # Skip system messages for this display
        conversation_msgs = [msg for msg in history if msg.get('role') != 'system']
        self.logger.debug(f"Recent history: {conversation_msgs}")
        return "\n".join(f"{msg['role']}: {msg['content']}" for msg in conversation_msgs[-n:])

    def show_sources(self) -> str:
        """Display sources from the last query."""
        if hasattr(self, '_last_sources') and self._last_sources:
            sources_text = "📚 **Sources from last query:**\n"
            for source in self._last_sources:
                sources_text += f"  • {source}\n"
            return sources_text
        return "No sources available from the last query."

    def clear_memory(self) -> str:
        """Clear conversation memory."""
        self.memory_manager.clear_memory()
        return f"✅ Cleared conversation memory for session '{self.session_id}'."

    def repair_memory(self) -> str:
        """Repair conversation memory."""
        stats = self.memory_manager.repair_conversation()
        return (f"✅ Memory repair completed for session '{self.session_id}':\n"
                f"  • Messages before: {stats['messages_before']}\n"
                f"  • Messages after: {stats['messages_after']}\n" 
                f"  • Messages removed: {stats['messages_removed']}\n"
                f"  • Orphaned tool calls fixed: {stats['orphaned_tool_calls_fixed']}")

    def get_memory_stats(self) -> str:
        """Get memory statistics."""
        stats = self.memory_manager.get_memory_stats()
        stats_text = f"📊 **Memory Stats for session '{self.session_id}':**\n"
        stats_text += f"  • Total messages: {stats['total_messages']}\n"
        stats_text += f"  • System messages: {stats['system_messages']}\n"
        stats_text += f"  • Max items: {stats['max_items']}\n"
        if stats['messages_by_role']:
            stats_text += f"  • Messages by role: {stats['messages_by_role']}\n"
        if stats['issues']:
            stats_text += f"  • Issues: {', '.join(stats['issues'])}\n"
        return stats_text

    def detect_intent(self, user_input: str) -> dict:
        """
        Detect user intent and extract commands.
        This is a stub for future MarketFlow API integration.
        
        Args:
            user_input (str): User's input text
            
        Returns:
            dict: Intent information with type and parameters
        """
        user_input_lower = user_input.lower().strip()
        
        # CLI commands
        if user_input_lower in ['/sources', '/source']:
            return {'type': 'command', 'action': 'show_sources'}
        elif user_input_lower in ['/clear', '/clear_memory']:
            return {'type': 'command', 'action': 'clear_memory'}
        elif user_input_lower in ['/repair', '/repair_memory']:
            return {'type': 'command', 'action': 'repair_memory'}
        elif user_input_lower in ['/stats', '/memory_stats']:
            return {'type': 'command', 'action': 'memory_stats'}
        elif user_input_lower in ['/help', '/?']:
            return {'type': 'command', 'action': 'help'}
        elif user_input_lower in {'quit', 'exit', '/quit', '/exit'}:
            return {'type': 'command', 'action': 'quit'}
            
        # Future: MarketFlow-specific intents could be detected here
        # e.g., requests for specific analysis, data queries, etc.
        return {'type': 'query', 'text': user_input}

    def get_help_text(self) -> str:
        """Get help text for available commands."""
        return """🔧 **Available Commands:**
  • `/sources` - Show sources from the last query
  • `/clear` - Clear conversation memory  
  • `/repair` - Repair conversation memory
  • `/stats` - Show memory statistics
  • `/help` - Show this help message
  • `/quit` or `quit` - Exit the application

💡 **Tips:**
  • Ask questions about Wyckoff method and VPA
  • The system remembers your conversation history
  • Sources are automatically included in responses when available"""

    def synthesize_with_openai(self, question: str, chunks: List[dict], include_sources: bool = False) -> str:
        """Synthesizes an answer using OpenAI's LLM based on the provided question and context chunks.
        Args:
            question (str): The user's question.
            chunks (List[dict]): List of context chunks retrieved from the knowledge base.
            include_sources (bool): Whether to include source information in the response.
        Returns:
            str: The synthesized answer from the LLM.
        """
        try:
            recent_history = self.get_recent_history(n=5)
            self.logger.debug(f"Recent history for context:\n{recent_history}")
            self.logger.info(f"Synthesizing answer with OpenAI for question: {question}")
            
            # Build context with metadata
            context_parts = []
            sources = []
            
            for i, chunk in enumerate(chunks):
                text = chunk.get("text", "")
                metadata = chunk.get("metadata", {})
                
                # Extract source information
                source_info = f"Source {i+1}"
                if metadata:
                    source_parts = []
                    if metadata.get("source"):
                        source_parts.append(f"file: {metadata['source']}")
                    if metadata.get("page"):
                        source_parts.append(f"page: {metadata['page']}")
                    if source_parts:
                        source_info += f" ({', '.join(source_parts)})"
                
                sources.append(source_info)
                context_parts.append(f"[{source_info}]\n{text}")
            
            context = "\n\n".join(context_parts)
            self.logger.debug(f"Context for synthesis:\n{context}")

            # Get full conversation history for context
            conversation_history = self.memory_manager.get_history(limit=10)
            history_context = ""
            if len(conversation_history) > 1:  # More than just system message
                history_msgs = []
                for msg in conversation_history[1:]:  # Skip system message
                    role = msg.get('role', 'unknown')
                    content = msg.get('content', '')
                    if role in ['user', 'assistant']:
                        history_msgs.append(f"{role.capitalize()}: {content}")
                if history_msgs:
                    history_context = f"Previous conversation:\n{chr(10).join(history_msgs[-6:])}\n\n"

            prompt = (
                f"{self.system_prompt}\n\n"
                f"{history_context}"
                f"Knowledge base information:\n{context}\n\n"
                f"Current question: {question}\n\n"
                f"Instructions: Provide a clear, concise answer based on the knowledge base information above. "
                f"Reference specific sources when relevant."
            )

            if include_sources:
                prompt += f"\n\nAvailable sources:\n" + "\n".join(sources)

            self.logger.debug(f"Prompt sent to OpenAI:\n{prompt}")
            
            # Use OpenAI API
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            answer = response.choices[0].message.content.strip()
            
            # Store sources for potential display
            self._last_sources = sources
            
            self.logger.info("Received answer from OpenAI.")
            self.logger.debug(f"Answer: {answer}")
            return answer
            
        except Exception as e:
            self.logger.error(f"Error during LLM synthesis: {e}")
            raise

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Minimal RAG Q&A system for Wyckoff and VPA knowledge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python minimal_rag.py                          # Use default session
  python minimal_rag.py --session user123       # Use specific session
  python minimal_rag.py --model gpt-4           # Use specific model
  python minimal_rag.py --system-prompt "You are an expert trader"  # Custom prompt
        """
    )
    
    parser.add_argument(
        '--session', '--session-id', '--user-id',
        type=str, 
        default='default',
        help='Session ID or User ID for memory management (default: default)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='OpenAI model to use (if not specified, uses config default)'
    )
    
    parser.add_argument(
        '--system-prompt',
        type=str,
        help='Custom system prompt to initialize the session'
    )
    
    parser.add_argument(
        '--history-limit',
        type=int,
        default=5,
        help='Number of recent messages to include in context (default: 5)'
    )
    
    return parser.parse_args()

def main():
    """Main interactive RAG Q&A loop."""
    try:
        args = parse_arguments()
        
        # Initialize RAG QA system
        rag_qa = MinimalRAGQA(
            model=args.model,
            session_id=args.session,
            system_prompt=args.system_prompt
        )
        
        print("🟢 Wyckoff & VPA RAG Q&A (Anna Coulling, etc)")
        print(f"📝 Session: {args.session}")
        print("Ask anything about Wyckoff, VPA, Anna Coulling's book.")
        print("Type '/help' for commands or 'quit' to exit.\n")
        
        rag_qa.logger.info(f"Started interactive RAG Q&A session for session: {args.session}")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                
                # Detect intent and handle commands
                intent = rag_qa.detect_intent(user_input)
                
                if intent['type'] == 'command':
                    action = intent['action']
                    
                    if action == 'quit':
                        print("👋 Goodbye!")
                        rag_qa.logger.info("User exited the session.")
                        break
                    elif action == 'show_sources':
                        print(rag_qa.show_sources())
                        continue
                    elif action == 'clear_memory':
                        print(rag_qa.clear_memory())
                        continue
                    elif action == 'repair_memory':
                        print(rag_qa.repair_memory())
                        continue
                    elif action == 'memory_stats':
                        print(rag_qa.get_memory_stats())
                        continue
                    elif action == 'help':
                        print(rag_qa.get_help_text())
                        continue
                
                # Handle regular queries
                user_q = intent['text']
                rag_qa.memory_manager.add_message(role="user", content=user_q)
                rag_qa.logger.info(f"Received user question: {user_q}")
                
                # Retrieve relevant chunks
                try:
                    top_chunks = chroma_retrieve_top_chunks(user_q, top_k=5)
                    rag_qa.logger.debug(f"Retrieved {len(top_chunks)} chunks")
                except Exception as e:
                    rag_qa.logger.error(f"Error retrieving chunks: {e}")
                    top_chunks = []
                
                if not top_chunks:
                    response = "Sorry, I couldn't find anything relevant in the knowledge base."
                    print(f"\nAI: {response}")
                    rag_qa.memory_manager.add_message(role="assistant", content=response)
                    rag_qa.logger.info(f"No relevant chunks found for question: {user_q}")
                    continue
                
                # Synthesize answer
                try:
                    answer = rag_qa.synthesize_with_openai(user_q, top_chunks)
                    rag_qa.memory_manager.add_message(role="assistant", content=answer)
                    print(f"\nAI: {answer}")
                    rag_qa.logger.info("Successfully provided answer to user")
                    
                except Exception as e:
                    error_msg = f"Sorry, there was an error generating the answer: {str(e)}"
                    print(f"\nAI: {error_msg}")
                    rag_qa.memory_manager.add_message(role="assistant", content=error_msg)
                    rag_qa.logger.error(f"Error during synthesis: {e}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                rag_qa.logger.info("Session interrupted by user")
                break
            except Exception as e:
                rag_qa.logger.error(f"Unexpected error in main loop: {e}")
                print(f"An unexpected error occurred: {e}")
                
    except Exception as e:
        print(f"Failed to initialize RAG QA system: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")

