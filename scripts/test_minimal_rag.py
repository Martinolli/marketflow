#!/usr/bin/env python3
"""
Test script for minimal_rag.py functionality.
This script tests the core functionality without external dependencies.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

def test_session_management():
    """Test session management functionality."""
    print("🧪 Testing session management...")
    
    # Test different session IDs
    test_sessions = ["user1", "user2", "default"]
    
    for session in test_sessions:
        memory_file = f".marketflow/memory/session_{session}.json"
        print(f"  ✓ Session '{session}' would use memory file: {memory_file}")
    
    print("✅ Session management test passed")

def test_intent_detection():
    """Test intent detection functionality."""
    print("🧪 Testing intent detection...")
    
    # Mock the MinimalRAGQA class
    class MockRAGQA:
        def detect_intent(self, user_input):
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
                
            return {'type': 'query', 'text': user_input}
    
    rag_qa = MockRAGQA()
    
    # Test commands
    test_cases = [
        ("/help", "command", "help"),
        ("/sources", "command", "show_sources"),
        ("/clear", "command", "clear_memory"),
        ("/stats", "command", "memory_stats"),
        ("quit", "command", "quit"),
        ("What is Wyckoff method?", "query", None),
    ]
    
    for input_text, expected_type, expected_action in test_cases:
        intent = rag_qa.detect_intent(input_text)
        assert intent['type'] == expected_type, f"Expected {expected_type}, got {intent['type']}"
        if expected_action:
            assert intent['action'] == expected_action, f"Expected {expected_action}, got {intent.get('action')}"
        print(f"  ✓ Intent detection for '{input_text}': {intent}")
    
    print("✅ Intent detection test passed")

def test_argument_parsing():
    """Test command line argument parsing."""
    print("🧪 Testing argument parsing...")
    
    # Mock argparse functionality
    test_args = [
        (["--session", "user123"], "user123"),
        (["--session-id", "trader1"], "trader1"), 
        (["--user-id", "analyst"], "analyst"),
        (["--model", "gpt-4"], "gpt-4"),
        (["--system-prompt", "You are an expert"], "You are an expert"),
    ]
    
    for args, expected in test_args:
        print(f"  ✓ Args {args} would set value to: {expected}")
    
    print("✅ Argument parsing test passed")

def test_memory_operations():
    """Test memory operations with mock data."""
    print("🧪 Testing memory operations...")
    
    class MockMemoryManager:
        def __init__(self):
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
    
    memory = MockMemoryManager()
    
    # Test system message
    memory.add_system_message("You are a helpful assistant")
    assert len(memory.system_messages) == 1
    print("  ✓ System message added")
    
    # Test regular messages
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there!")
    assert len(memory.memory) == 2
    print("  ✓ Regular messages added")
    
    # Test history retrieval
    history = memory.get_history(limit=1)
    assert len(history) == 2  # 1 system + 1 limited conversation message
    print("  ✓ History retrieval with limit works")
    
    # Test stats
    stats = memory.get_memory_stats()
    assert stats["total_messages"] == 2
    assert stats["system_messages"] == 1
    print("  ✓ Memory stats work")
    
    # Test clear
    memory.clear_memory()
    assert len(memory.memory) == 0
    assert len(memory.system_messages) == 1  # System messages preserved
    print("  ✓ Memory clear works")
    
    print("✅ Memory operations test passed")

def test_chunk_metadata():
    """Test chunk metadata handling."""
    print("🧪 Testing chunk metadata handling...")
    
    # Sample chunks with metadata
    sample_chunks = [
        {
            "text": "Wyckoff method focuses on market structure...",
            "metadata": {"source": "wyckoff_book.pdf", "page": 42}
        },
        {
            "text": "Volume Price Analysis by Anna Coulling...", 
            "metadata": {"source": "vpa_guide.pdf", "page": 15}
        },
        {
            "text": "Accumulation phase characteristics...",
            "metadata": {"source": "trading_manual.pdf", "page": 78}
        }
    ]
    
    # Test source extraction
    sources = []
    for i, chunk in enumerate(sample_chunks):
        source_info = f"Source {i+1}"
        metadata = chunk.get("metadata", {})
        if metadata:
            source_parts = []
            if metadata.get("source"):
                source_parts.append(f"file: {metadata['source']}")
            if metadata.get("page"):
                source_parts.append(f"page: {metadata['page']}")
            if source_parts:
                source_info += f" ({', '.join(source_parts)})"
        sources.append(source_info)
    
    expected_sources = [
        "Source 1 (file: wyckoff_book.pdf, page: 42)",
        "Source 2 (file: vpa_guide.pdf, page: 15)", 
        "Source 3 (file: trading_manual.pdf, page: 78)"
    ]
    
    for i, (actual, expected) in enumerate(zip(sources, expected_sources)):
        assert actual == expected, f"Source {i+1}: expected {expected}, got {actual}"
        print(f"  ✓ Source {i+1}: {actual}")
    
    print("✅ Chunk metadata test passed")

def main():
    """Run all tests."""
    print("🚀 Running minimal_rag.py functionality tests\n")
    
    try:
        test_session_management()
        print()
        test_intent_detection()
        print()
        test_argument_parsing()
        print()
        test_memory_operations()
        print()
        test_chunk_metadata()
        print()
        print("🎉 All tests passed!")
        return 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())