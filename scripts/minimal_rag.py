#!/usr/bin/env python3
"""
Enhanced Minimal RAG QA Script with Session Management and Extended Features

This script provides a foundational RAG-based Q&A system with:
- Session/user management support
- Customizable system prompts
- Enhanced memory management
- RAG chunk metadata display  
- Error handling and logging
- Extensibility hooks for future MarketFlow integration
"""

import os
import sys
import argparse  
import openai
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from rag.retriever import chroma_retrieve_top_chunks  # adjust import if needed
from marketflow.marketflow_config_manager import ConfigManager, create_app_config  # adjust import if needed
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_memory_manager import MemoryManager

class MinimalRAGQA:
    """Enhanced RAG QA system with session management and extensibility hooks."""
    
    def __init__(self, model: Optional[str] = None, session_id: str = "default", 
                 system_prompt: Optional[str] = None) -> None:
        """Initialize the MinimalRAGQA class.
        Args:
            model (str, optional): The OpenAI model to use for synthesis.
            session_id (str): Session identifier for memory management.
            system_prompt (str, optional): Custom system prompt for the LLM.
        """
        try:
            # Initialize logger
            self.logger = get_logger("MinimalRAGQA")
            
            # Store session info
            self.session_id = session_id
            
            # Initialize configuration manager
            self.config_manager = create_app_config(logger=self.logger)
            self.logger.info("Configuration manager initialized.")
            
            # Set up model
            self.model = model or self.config_manager.get_llm_model()
            if not self.model:
                raise ValueError("No LLM model configured.")
            
            # Log the initialization
            self.logger.info(f"Initialized MinimalRAGQA with model: {self.model}, session: {session_id}")
            
            # Initialize memory manager with session-specific file
            memory_file = f".marketflow/memory/session_{session_id}.json"
            self.memory_manager = MemoryManager(memory_file=memory_file)
            self.logger.info(f"Memory manager initialized with file: {memory_file}")
            
            # Set up system prompt
            self.system_prompt = system_prompt or self._get_default_system_prompt()
            if self.system_prompt:
                self.memory_manager.add_system_message(self.system_prompt)
                self.logger.info("System prompt added to memory manager")
                
        except Exception as e:
            self.logger.error(f"Error initializing MinimalRAGQA: {e}")
            raise
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the assistant."""
        return (
            "You are an expert assistant specializing in Wyckoff methodology and "
            "Anna Coulling's Volume Price Analysis (VPA). You provide clear, "
            "accurate answers based on the provided context and conversation history. "
            "When citing information, reference the source materials when available."
        )

    def get_recent_history(self, n: int = 5) -> str:
        """Get the last n messages from memory and concatenate them for context.
        Args:
            n (int): Number of recent messages to retrieve.
        Returns:
            str: Concatenated string of the last n messages.
        """
        try:
            history = self.memory_manager.get_history(limit=n)
            # Filter out system messages for context display
            conversation_history = [msg for msg in history if msg.get('role') != 'system'][-n:]
            self.logger.debug(f"Recent history: {len(conversation_history)} messages")
            return "\n".join(f"{msg['role']}: {msg['content']}" for msg in conversation_history)
        except Exception as e:
            self.logger.error(f"Error retrieving recent history: {e}")
            return ""
    
    def clear_memory(self) -> None:
        """Clear conversation memory while preserving system messages."""
        try:
            self.memory_manager.clear_memory()
            self.logger.info("Memory cleared successfully")
            print("✅ Conversation memory cleared.")
        except Exception as e:
            self.logger.error(f"Error clearing memory: {e}")
            print(f"❌ Error clearing memory: {e}")
    
    def repair_memory(self) -> None:
        """Repair conversation memory by fixing any issues."""
        try:
            repair_stats = self.memory_manager.repair_conversation()
            self.logger.info(f"Memory repair completed: {repair_stats}")
            print(f"✅ Memory repaired: {repair_stats}")
        except Exception as e:
            self.logger.error(f"Error repairing memory: {e}")
            print(f"❌ Error repairing memory: {e}")
    
    def show_memory_stats(self) -> None:
        """Display current memory statistics."""
        try:
            stats = self.memory_manager.get_memory_stats()
            print("\n📊 Memory Statistics:")
            print(f"  Total messages: {stats['total_messages']}")
            print(f"  System messages: {stats['system_messages']}")
            print(f"  Memory file: {stats['memory_file']}")
            print(f"  Max items: {stats['max_items']}")
            
            if stats.get('messages_by_role'):
                print("  Messages by role:")
                for role, count in stats['messages_by_role'].items():
                    print(f"    {role}: {count}")
            
            if stats.get('issues'):
                print("  Issues:")
                for issue in stats['issues']:
                    print(f"    ⚠️ {issue}")
        except Exception as e:
            self.logger.error(f"Error getting memory stats: {e}")
            print(f"❌ Error getting memory stats: {e}")
    
    def display_sources(self, chunks: List[Dict[str, Any]]) -> None:
        """Display source information from retrieved chunks."""
        if not chunks:
            print("No sources available.")
            return
            
        print("\n📚 Sources:")
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get('metadata', {})
            source = metadata.get('source', 'Unknown')
            page = metadata.get('page', 'N/A')
            distance = chunk.get('distance', chunk.get('score', 'N/A'))
            print(f"  {i}. {source} (Page: {page}, Relevance: {distance:.4f})")
    
    # Extensibility hooks for future MarketFlow integration
    def detect_intent(self, user_input: str) -> str:
        """
        Detect user intent for potential routing to specialized handlers.
        
        This is a stub for future integration with MarketFlow-specific
        intent detection and routing logic.
        
        Args:
            user_input (str): The user's input text
            
        Returns:
            str: Detected intent (currently always 'general_query')
        """
        # TODO: Implement intent detection logic
        # Could include patterns for:
        # - Market analysis requests
        # - Chart pattern queries  
        # - Wyckoff phase identification
        # - VPA-specific questions
        self.logger.debug(f"Intent detection stub called for: {user_input[:50]}...")
        return "general_query"
    
    def call_marketflow_api(self, intent: str, query: str) -> Optional[str]:
        """
        Integration point for MarketFlow API calls.
        
        This is a stub for future integration with MarketFlow analysis
        and data retrieval APIs.
        
        Args:
            intent (str): The detected intent
            query (str): The user's query
            
        Returns:
            Optional[str]: API response or None if not applicable
        """
        # TODO: Implement MarketFlow API integration
        # Could include calls to:
        # - Market data providers
        # - Technical analysis engines
        # - Pattern recognition systems
        self.logger.debug(f"MarketFlow API stub called for intent '{intent}': {query[:50]}...")
        return None

    def synthesize_with_openai(self, question: str, chunks: List[Dict[str, Any]]) -> str:
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
            
            # Build context with metadata
            context_with_sources = []
            for i, chunk in enumerate(chunks, 1):
                text = chunk.get("text", "")
                metadata = chunk.get("metadata", {})
                source = metadata.get('source', 'Unknown')
                page = metadata.get('page', 'N/A')
                
                context_entry = f"[Source {i}: {source}, Page {page}]\n{text}"
                context_with_sources.append(context_entry)
            
            context = "\n\n".join(context_with_sources)
            self.logger.debug(f"Context for synthesis (with sources):\n{context[:500]}...")

            # Build enhanced prompt with system context
            prompt = self._build_synthesis_prompt(question, context, recent_history)
            
            self.logger.debug(f"Prompt sent to OpenAI:\n{prompt[:500]}...")
            
            # Call OpenAI API with error handling
            answer = self._call_openai_api(prompt)
            
            self.logger.info("Successfully received answer from OpenAI.")
            self.logger.debug(f"Answer: {answer}")
            return answer
            
        except Exception as e:
            self.logger.error(f"Error during LLM synthesis: {e}")
            raise
    
    def _build_synthesis_prompt(self, question: str, context: str, recent_history: str) -> str:
        """Build the synthesis prompt with context threading."""
        prompt_parts = []
        
        # Add recent conversation context if available
        if recent_history.strip():
            prompt_parts.append(f"Previous conversation context:\n{recent_history}\n")
        
        # Add the main context
        prompt_parts.append(f"Relevant information from knowledge base:\n---\n{context}\n---\n")
        
        # Add the question
        prompt_parts.append(f"**Question:** {question}\n")
        
        # Add instructions
        prompt_parts.append(
            "Please provide a clear, concise answer based on the information provided. "
            "Reference specific sources when relevant. If the information is insufficient "
            "to fully answer the question, acknowledge this limitation."
        )
        
        return "\n".join(prompt_parts)
    
    def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI API with proper error handling and retries."""
        try:
            # For openai>=1.x
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            return response.choices[0].message.content.strip()
            
        except AttributeError:
            # For openai==0.x (fallback)
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.6,
            )
            return response.choices[0].message["content"].strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {e}")
            raise

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Enhanced Minimal RAG QA System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --session john --system-prompt "You are a trading expert"
  %(prog)s --session analysis_session --model gpt-4
  
Special Commands (during interactive session):
  /clear     - Clear conversation memory
  /repair    - Repair conversation memory
  /stats     - Show memory statistics
  /sources   - Show sources from last query
  /help      - Show this help
  quit/exit  - Exit the program
        """
    )
    
    parser.add_argument(
        "--session", "--session-id", "--user",
        default="default",
        help="Session/user identifier for memory management (default: default)"
    )
    
    parser.add_argument(
        "--model",
        help="OpenAI model to use (overrides config)"
    )
    
    parser.add_argument(
        "--system-prompt", 
        help="Custom system prompt for the assistant"
    )
    
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of top chunks to retrieve from knowledge base (default: 5)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser.parse_args()

def handle_special_command(command: str, rag_qa: MinimalRAGQA, last_chunks: List[Dict[str, Any]]) -> bool:
    """Handle special CLI commands. Returns True if command was handled."""
    command = command.lower().strip()
    
    if command == "/clear":
        rag_qa.clear_memory()
        return True
    elif command == "/repair":
        rag_qa.repair_memory()
        return True
    elif command == "/stats":
        rag_qa.show_memory_stats()
        return True
    elif command == "/sources":
        rag_qa.display_sources(last_chunks)
        return True
    elif command == "/help":
        print("""
💡 Special Commands:
  /clear     - Clear conversation memory
  /repair    - Repair conversation memory
  /stats     - Show memory statistics  
  /sources   - Show sources from last query
  /help      - Show this help
  quit/exit  - Exit the program
        """)
        return True
    
    return False

def main():
    """Main interactive RAG QA session with enhanced features."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set up logging level
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Initialize RAG QA system
        print(f"🔧 Initializing RAG QA system (session: {args.session})...")
        rag_qa = MinimalRAGQA(
            model=args.model,
            session_id=args.session,
            system_prompt=args.system_prompt
        )
        
        # Display welcome message
        print("🟢 Enhanced Wyckoff & VPA RAG Q&A System")
        print("Ask anything about Wyckoff, VPA, Anna Coulling's methods.")
        print("Type '/help' for special commands or 'quit' to exit.\n")
        
        rag_qa.logger.info(f"Started interactive RAG Q&A session (session: {args.session})")
        
        last_chunks = []  # Store last retrieved chunks for /sources command
        
        while True:
            try:
                user_q = input("You: ").strip()
                
                if not user_q:
                    continue
                
                # Handle special commands
                if user_q.startswith('/'):
                    if handle_special_command(user_q, rag_qa, last_chunks):
                        continue
                    else:
                        print(f"❌ Unknown command: {user_q}. Type '/help' for available commands.")
                        continue
                
                # Check for exit
                if user_q.lower() in {"quit", "exit"}:
                    print("Goodbye!")
                    rag_qa.logger.info("User exited the session.")
                    break
                
                # Store user question in memory
                rag_qa.memory_manager.add_message(role="user", content=user_q)
                rag_qa.logger.info(f"Received user question: {user_q}")
                
                # Detect intent (extensibility hook)
                intent = rag_qa.detect_intent(user_q)
                
                # Try MarketFlow API integration (extensibility hook)
                api_response = rag_qa.call_marketflow_api(intent, user_q)
                if api_response:
                    print(f"\n🔍 MarketFlow Analysis: {api_response}")
                
                # Retrieve relevant chunks
                print("🔍 Searching knowledge base...")
                top_chunks = chroma_retrieve_top_chunks(user_q, top_k=args.top_k)
                last_chunks = top_chunks  # Store for /sources command
                
                rag_qa.logger.debug(f"Retrieved {len(top_chunks)} chunks")
                
                if not top_chunks:
                    print("AI: Sorry, I couldn't find anything relevant in the knowledge base.")
                    rag_qa.logger.info(f"No relevant chunks found for question: {user_q}")
                    continue
                
                # Synthesize answer with LLM
                print("🤖 Generating response...")
                answer = rag_qa.synthesize_with_openai(user_q, top_chunks)
                
                # Store the answer in memory
                rag_qa.memory_manager.add_message(role="assistant", content=answer)
                rag_qa.logger.info("Answer generated and stored in memory")
                
                # Display the answer
                print(f"\nAI: {answer}")
                
                # Optionally show quick source info
                if len(top_chunks) > 0:
                    print(f"\n📚 Found {len(top_chunks)} relevant source(s). Type '/sources' to see details.")
                
            except KeyboardInterrupt:
                print("\n\nUse 'quit' or 'exit' to leave gracefully.")
                continue
            except Exception as e:
                rag_qa.logger.error(f"Error processing query: {e}")
                print(f"❌ Sorry, there was an error processing your request: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
