"""
Memory Manager Module for VPA Query Engine - COMPATIBLE VERSION

This module provides memory management functionality for the VPA Query Engine,
compatible with the existing vpa_app.py interface while including all the fixes
for conversation validation and orphaned tool call cleanup.

COMPATIBILITY FEATURES:
1. Supports both 'db_path' and 'memory_file' parameters for backward compatibility
2. Maintains the same interface as the original memory manager
3. Includes all the critical fixes for OpenAI API compliance
4. Enhanced error handling and conversation validation
"""

import os
import json
import time
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config



class MemoryManager:
    """
    Memory manager for VPA Query Engine with robust conversation validation.
    
    This version ensures OpenAI API compliance by validating that every assistant
    message with tool_calls has corresponding function responses.
    
    BACKWARD COMPATIBILITY: Supports both db_path and memory_file parameters.
    """
    
    def __init__(self, memory_file: Optional[str] = None, db_path: Optional[str] = None, 
                 max_memory_items: int = 100, is_test_env: bool = False):
        """
        Initialize the Memory Manager with backward compatibility
        
        Parameters:
        - memory_file: Path to memory storage file (new parameter name)
        - db_path: Path to memory storage file (legacy parameter name for compatibility)
        - max_memory_items: Maximum number of memory items to store
        - is_test_env: Whether running in test environment
        """
        # Initialize logging and configuration
        self.logger = get_logger(module_name="MarketflowMemoryManager")
        self.config_manager = create_app_config(logger=self.logger)

        self.logger.info("Initializing Enhanced MarketFlow Memory Manager")

        # Handle backward compatibility for db_path parameter
        if memory_file is None and db_path is not None:
            memory_file = db_path
            self.logger.debug("Using db_path parameter for backward compatibility")
        
        # Set memory file path
        if memory_file is None:
            if is_test_env:
                # Use temporary file for testing
                temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
                memory_file = temp_file.name
                temp_file.close()
            else:
                # Use the correct pathway as specified for production use
                memory_dir = r"C:\Users\Aspire5 15 i7 4G2050\marketflow\.marketflow\memory"
                os.makedirs(memory_dir, exist_ok=True)
                memory_file = os.path.join(memory_dir, "marketflow_memory.json")

        self.memory_file = memory_file
        self.max_memory_items = max_memory_items
        self.system_messages = []  # Separate storage for system messages
        
        # Initialize memory storage
        self.memory = self._load_memory()
        
        # Validate and fix conversation integrity
        self._validate_and_fix_conversation()
    
    def _load_memory(self) -> List[Dict[str, Any]]:
        """Load memory from file with error handling"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    memory = json.load(f)
                self.logger.debug(f"Loaded {len(memory)} memory items from {self.memory_file}")
                return memory
            else:
                self.logger.debug(f"Memory file {self.memory_file} not found, initializing empty memory")
                return []
        except Exception as e:
            self.logger.error(f"Error loading memory from {self.memory_file}: {e}")
            self.logger.warning("Starting with empty memory due to load error")
            return []
    
    def _save_memory(self) -> None:
        """Save memory to file with proper JSON serialization"""
        try:
            # Create a serializable copy of memory
            serializable_memory = []
            for item in self.memory:
                serializable_item = {}
                for key, value in item.items():
                    if key == 'tool_calls' and value:
                        # Convert tool calls to serializable format
                        serializable_item[key] = self._serialize_tool_calls(value)
                    else:
                        # Handle other non-serializable objects
                        try:
                            json.dumps(value)  # Test if it's serializable
                            serializable_item[key] = value
                        except (TypeError, ValueError):
                            # Convert to string if not serializable
                            serializable_item[key] = str(value)
                serializable_memory.append(serializable_item)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            
            with open(self.memory_file, 'w') as f:
                json.dump(serializable_memory, f, indent=2)
            self.logger.debug(f"Saved {len(serializable_memory)} memory items to {self.memory_file}")
        except Exception as e:
            self.logger.error(f"Error saving memory to {self.memory_file}: {e}")
    
    def _serialize_tool_calls(self, tool_calls) -> List[Dict[str, Any]]:
        """Convert tool calls to a JSON-serializable format"""
        serializable_calls = []
        for call in tool_calls:
            if hasattr(call, '__dict__'):
                # Handle objects with attributes
                call_dict = {
                    'id': getattr(call, 'id', None),
                    'type': getattr(call, 'type', 'function'),
                    'function': {
                        'name': getattr(call.function, 'name', None) if hasattr(call, 'function') else None,
                        'arguments': getattr(call.function, 'arguments', None) if hasattr(call, 'function') else None
                    }
                }
            else:
                # Handle dictionaries or other formats
                call_dict = dict(call) if hasattr(call, 'items') else {'raw': str(call)}
            
            serializable_calls.append(call_dict)
        
        return serializable_calls
    
    def _validate_and_fix_conversation(self) -> None:
        """
        Validate conversation integrity and fix OpenAI API compliance issues.
        
        This method ensures that every assistant message with tool_calls has
        corresponding function responses, preventing OpenAI API errors.
        """
        if not self.memory:
            return
        
        original_length = len(self.memory)
        fixed_memory = []
        orphaned_tool_calls = []
        
        i = 0
        while i < len(self.memory):
            message = self.memory[i]
            
            # Check if this is an assistant message with tool calls
            if (message.get('role') == 'assistant' and 
                message.get('tool_calls') and 
                len(message.get('tool_calls', [])) > 0):
                
                # Find corresponding function responses
                tool_call_ids = []
                for tool_call in message.get('tool_calls', []):
                    if isinstance(tool_call, dict):
                        tool_call_ids.append(tool_call.get('id'))
                    else:
                        tool_call_ids.append(getattr(tool_call, 'id', None))
                
                # Look for function responses immediately following
                function_responses = []
                j = i + 1
                while j < len(self.memory) and self.memory[j].get('role') == 'function':
                    func_msg = self.memory[j]
                    if func_msg.get('tool_call_id') in tool_call_ids:
                        function_responses.append(func_msg)
                        tool_call_ids.remove(func_msg.get('tool_call_id'))
                    j += 1
                
                # If we have orphaned tool calls, handle them
                if tool_call_ids:
                    self.logger.warning(f"Found orphaned tool calls: {tool_call_ids}")
                    orphaned_tool_calls.extend(tool_call_ids)
                    
                    # Option 1: Skip this assistant message entirely
                    self.logger.info(f"Removing assistant message with orphaned tool calls")
                    i += 1
                    continue
                
                # Add the assistant message and its function responses
                fixed_memory.append(message)
                for func_resp in function_responses:
                    fixed_memory.append(func_resp)
                
                # Skip past the function responses we've already processed
                i = j
            else:
                # Regular message, just add it
                fixed_memory.append(message)
                i += 1
        
        # Update memory if we made changes
        if len(fixed_memory) != original_length or orphaned_tool_calls:
            self.memory = fixed_memory
            self._save_memory()
            
            if orphaned_tool_calls:
                self.logger.warning(f"Cleaned up {len(orphaned_tool_calls)} orphaned tool calls")
            
            if len(fixed_memory) != original_length:
                self.logger.info(f"Memory cleaned: {original_length} -> {len(fixed_memory)} messages")
    
    def _extract_function_name_from_content(self, content: str) -> Optional[str]:
        """Extract function name from content string"""
        if not content:
            return None
        
        # Try to parse as JSON
        try:
            data = json.loads(content)
            if isinstance(data, dict) and 'name' in data:
                name = data['name']
                # Handle "functions.function_name" format
                if name and isinstance(name, str) and name.startswith("functions."):
                    return name.split(".", 1)[1]
                return name
        except:
            pass
        
        # Try regex pattern matching
        import re
        name_match = re.search(r'"name"\s*:\s*"([^"]+)"', content)
        if name_match:
            name = name_match.group(1)
            if name.startswith("functions."):
                return name.split(".", 1)[1]
            return name
        
        return None
    
    def _validate_message_params(self, role: str, content: str, **kwargs) -> None:
        """Validate message parameters"""
        valid_roles = ['user', 'assistant', 'system', 'function']
        if role not in valid_roles:
            raise ValueError(f"Invalid role '{role}'. Must be one of: {valid_roles}")
        
        if not isinstance(content, str):
            content = str(content) if content is not None else ""
        
        # Validate function message requirements
        if role == 'function':
            if 'name' not in kwargs:
                raise ValueError("Function messages must include 'name' parameter")
            if 'tool_call_id' not in kwargs:
                self.logger.warning("Function message missing 'tool_call_id' - this may cause OpenAI API issues")
    
    def add_message(self, role: str, content: str, **kwargs) -> None:
        """
        Add a message to the conversation history with validation.
        
        Parameters:
        - role: Message role ('user', 'assistant', 'system', 'function')
        - content: Message content
        - **kwargs: Additional message properties (tool_calls, name, tool_call_id, etc.)
        """
        # Validate parameters
        self._validate_message_params(role, content, **kwargs)
        
        # Handle system messages specially
        if role == "system":
            self.add_system_message(content)
            return
        
        # Ensure content is a string
        if not isinstance(content, str):
            content = str(content) if content is not None else ""
        
        # Create message
        message = {"role": role, "content": content}
        
        # Handle tool_calls specially for proper serialization
        if 'tool_calls' in kwargs and kwargs['tool_calls']:
            message['tool_calls'] = kwargs['tool_calls']
        
        # Add other kwargs
        for key, value in kwargs.items():
            if key != 'tool_calls':  # Already handled above
                message[key] = value
        
        # Add to memory and save
        self.memory.append(message)
        self._trim_memory()
        self._save_memory()
        
        self.logger.debug(f"Added {role} message: {content[:50]}...")
    
    def add_tool_response(self, tool_call_id: str, function_name: str, function_response: str) -> None:
        """
        Add a tool response message to the conversation history.
        
        This method ensures proper formatting for function call responses.
        
        Parameters:
        - tool_call_id: The ID of the tool call this is responding to
        - function_name: The name of the function that was called
        - function_response: The response from the function (as a string)
        """
        if not tool_call_id:
            raise ValueError("tool_call_id is required for tool responses")
        if not function_name:
            raise ValueError("function_name is required for tool responses")
        if not isinstance(function_response, str):
            function_response = str(function_response)
        
        message = {
            "role": "function",
            "name": function_name,
            "content": function_response,
            "tool_call_id": tool_call_id
        }
        
        self.memory.append(message)
        self._trim_memory()
        self._save_memory()
        
        self.logger.debug(f"Added tool response for {function_name}: {function_response[:50]}...")
    
    def add_system_message(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Parameters:
        - content: System message content
        """
        if not isinstance(content, str):
            raise TypeError("System message content must be a string")
        
        message = {"role": "system", "content": content}
        self.system_messages.append(message)
        self.logger.info(f"Added system message: {content[:50]}...")
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history in OpenAI API format with validation.
        
        This method ensures the returned history is compliant with OpenAI API
        requirements, particularly around tool calls and function responses.
        
        Parameters:
        - limit: Optional limit on the number of conversation messages to return
        
        Returns:
        - List of message dictionaries with proper OpenAI API formatting
        """
        # Start with system messages (always included)
        history = list(self.system_messages)
        
        # Get conversation messages with optional limit
        if limit:
            recent_items = self.memory[-limit:] if self.memory else []
        else:
            recent_items = self.memory[-10:] if self.memory else []  # Default to last 10
        
        # Validate and format messages
        validated_messages = self._validate_conversation_for_openai(recent_items)
        
        # Process each validated message
        for item in validated_messages:
            if 'role' in item:
                # Create a clean copy
                message = {"role": item["role"]}
                
                # Ensure content is a string
                message["content"] = str(item.get('content', ''))
                
                # Handle special fields
                if 'tool_calls' in item and item['tool_calls']:
                    # Ensure tool_calls are serializable
                    message["tool_calls"] = self._serialize_tool_calls(item['tool_calls'])
                
                if item['role'] == 'function':
                    # Ensure function messages have required fields
                    message["name"] = item.get('name', 'unknown_function')
                    if 'tool_call_id' in item:
                        message["tool_call_id"] = item['tool_call_id']
                
                # Add other fields
                for key, value in item.items():
                    if key not in ['role', 'content', 'tool_calls', 'name', 'tool_call_id']:
                        message[key] = value
                
                history.append(message)
        
        return history
    
    def _validate_conversation_for_openai(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate conversation messages for OpenAI API compliance.
        
        Ensures that every assistant message with tool_calls has corresponding
        function responses.
        
        Parameters:
        - messages: List of conversation messages
        
        Returns:
        - List of validated messages safe for OpenAI API
        """
        if not messages:
            return []
        
        validated = []
        i = 0
        
        while i < len(messages):
            message = messages[i]
            
            # Check if this is an assistant message with tool calls
            if (message.get('role') == 'assistant' and 
                message.get('tool_calls') and 
                len(message.get('tool_calls', [])) > 0):
                
                # Collect tool call IDs
                tool_call_ids = set()
                for tool_call in message.get('tool_calls', []):
                    if isinstance(tool_call, dict):
                        tool_call_ids.add(tool_call.get('id'))
                    else:
                        tool_call_ids.add(getattr(tool_call, 'id', None))
                
                # Look for corresponding function responses
                function_responses = []
                j = i + 1
                found_tool_call_ids = set()
                
                while j < len(messages) and messages[j].get('role') == 'function':
                    func_msg = messages[j]
                    func_tool_call_id = func_msg.get('tool_call_id')
                    
                    if func_tool_call_id in tool_call_ids:
                        function_responses.append(func_msg)
                        found_tool_call_ids.add(func_tool_call_id)
                    
                    j += 1
                
                # Only include if all tool calls have responses
                if found_tool_call_ids == tool_call_ids:
                    validated.append(message)
                    validated.extend(function_responses)
                    i = j
                else:
                    # Skip this assistant message and its partial responses
                    missing_ids = tool_call_ids - found_tool_call_ids
                    self.logger.warning(f"Skipping assistant message with missing tool responses: {missing_ids}")
                    i = j
            else:
                # Regular message, include it
                validated.append(message)
                i += 1
        
        return validated
    
    def _trim_memory(self) -> None:
        """Trim memory to maximum size if needed"""
        if len(self.memory) > self.max_memory_items:
            removed_count = len(self.memory) - self.max_memory_items
            self.memory = self.memory[-self.max_memory_items:]
            self.logger.debug(f"Trimmed {removed_count} old messages from memory")
    
    def clear_memory(self) -> None:
        """Clear all conversation memory (but keep system messages)"""
        self.memory = []
        self._save_memory()
        self.logger.info("Cleared conversation memory")
    
    def clear_system_messages(self) -> None:
        """Clear all system messages"""
        self.system_messages = []
        self.logger.info("Cleared system messages")
    
    def clear_all(self) -> None:
        """Clear both conversation memory and system messages"""
        self.clear_memory()
        self.clear_system_messages()
        self.logger.info("Cleared all memory")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about the current memory state"""
        stats = {
            "total_messages": len(self.memory),
            "system_messages": len(self.system_messages),
            "memory_file": self.memory_file,
            "max_items": self.max_memory_items
        }
        
        # Count messages by role
        role_counts = {}
        for item in self.memory:
            role = item.get('role', 'unknown')
            role_counts[role] = role_counts.get(role, 0) + 1
        
        stats["messages_by_role"] = role_counts
        
        # Check for potential issues
        issues = []
        orphaned_tool_calls = self._check_for_orphaned_tool_calls()
        if orphaned_tool_calls:
            issues.append(f"Found {len(orphaned_tool_calls)} orphaned tool calls")
        
        stats["issues"] = issues
        
        return stats
    
    def _check_for_orphaned_tool_calls(self) -> List[str]:
        """Check for orphaned tool calls in memory"""
        orphaned = []
        
        for i, message in enumerate(self.memory):
            if (message.get('role') == 'assistant' and 
                message.get('tool_calls') and 
                len(message.get('tool_calls', [])) > 0):
                
                # Get tool call IDs
                tool_call_ids = set()
                for tool_call in message.get('tool_calls', []):
                    if isinstance(tool_call, dict):
                        tool_call_ids.add(tool_call.get('id'))
                    else:
                        tool_call_ids.add(getattr(tool_call, 'id', None))
                
                # Look for function responses
                j = i + 1
                while j < len(self.memory) and self.memory[j].get('role') == 'function':
                    func_msg = self.memory[j]
                    func_tool_call_id = func_msg.get('tool_call_id')
                    if func_tool_call_id in tool_call_ids:
                        tool_call_ids.remove(func_tool_call_id)
                    j += 1
                
                # Any remaining IDs are orphaned
                orphaned.extend(list(tool_call_ids))
        
        return orphaned
    
    def repair_conversation(self) -> Dict[str, Any]:
        """
        Repair conversation by removing orphaned tool calls and fixing issues.
        
        Returns:
        - Dictionary with repair statistics
        """
        original_length = len(self.memory)
        orphaned_before = self._check_for_orphaned_tool_calls()
        
        # Run validation and fix
        self._validate_and_fix_conversation()
        
        orphaned_after = self._check_for_orphaned_tool_calls()
        final_length = len(self.memory)
        
        repair_stats = {
            "messages_before": original_length,
            "messages_after": final_length,
            "messages_removed": original_length - final_length,
            "orphaned_tool_calls_before": len(orphaned_before),
            "orphaned_tool_calls_after": len(orphaned_after),
            "orphaned_tool_calls_fixed": len(orphaned_before) - len(orphaned_after)
        }
        
        self.logger.info(f"Conversation repair completed: {repair_stats}")
        return repair_stats

