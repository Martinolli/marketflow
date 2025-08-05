# Enhanced Minimal RAG Q&A System

This enhanced version of `minimal_rag.py` provides a robust foundation for LLM-driven RAG Q&A with session management and extensibility hooks for MarketFlow integration.

## New Features

### 1. Session/User Management
- **Session-specific memory**: Each user/session gets their own memory file
- **CLI arguments**: `--session`, `--session-id`, or `--user-id` to specify session
- **Default session**: Uses 'default' if no session specified
- **Memory isolation**: Sessions are completely isolated from each other

### 2. MemoryManager Integration
- **System message initialization**: Automatically sets up system prompts per session
- **Memory commands**: `/clear`, `/repair`, `/stats` for memory management
- **Custom history limits**: Configurable conversation context length
- **Persistent storage**: Conversations survive application restarts

### 3. RAG Chunk Metadata
- **Source information**: Displays file names, page numbers, and other metadata
- **Context enhancement**: Metadata included in LLM prompts for better responses
- **Sources command**: `/sources` to show sources from last query
- **Rich context**: Combines metadata with text for comprehensive answers

### 4. Prompt Engineering
- **Customizable system prompt**: Use `--system-prompt` argument
- **Multi-turn context**: Includes conversation history in prompts
- **Structured prompts**: Clear separation of context, history, and questions
- **Source referencing**: LLM instructed to reference specific sources

### 5. Enhanced CLI Interface
- **Command detection**: Automatic detection of commands vs queries
- **Help system**: `/help` shows all available commands
- **Error handling**: Graceful handling of errors with user feedback
- **Rich output**: Emojis and formatting for better user experience

### 6. Extensibility Hooks
- **Intent detection**: Stub for future MarketFlow API integration
- **Command framework**: Easy to add new commands
- **Modular design**: Components can be extended or replaced
- **Configuration support**: Works with MarketFlow config system

## Usage Examples

### Basic Usage
```bash
# Default session
python scripts/minimal_rag.py

# Specific session
python scripts/minimal_rag.py --session trader123

# Custom model and prompt
python scripts/minimal_rag.py --model gpt-4 --system-prompt "You are an expert trader"
```

### Available Commands
- `/help` - Show help and available commands
- `/sources` - Show sources from the last query  
- `/clear` - Clear conversation memory for current session
- `/repair` - Repair conversation memory (fix orphaned tool calls)
- `/stats` - Show memory statistics for current session
- `quit` or `/quit` - Exit the application

### Session Management
```bash
# User sessions
python scripts/minimal_rag.py --session user1
python scripts/minimal_rag.py --session user2

# Each session has independent memory in:
# .marketflow/memory/session_user1.json
# .marketflow/memory/session_user2.json
```

## Dependencies

### Required
- `openai` - For LLM synthesis
- `argparse` - For CLI argument parsing (built-in)

### Optional (with graceful fallbacks)
- `chromadb` - For vector similarity search
- `pandas` - For MarketFlow config system
- `polygon-api-client` - For MarketFlow data provider

### MarketFlow Integration
- `marketflow.marketflow_logger` - For consistent logging
- `marketflow.marketflow_memory_manager` - For conversation memory
- `marketflow.marketflow_config_manager` - For configuration
- `rag.retriever` - For document retrieval

## Architecture

### Core Components
1. **MinimalRAGQA**: Main application class with session management
2. **MemoryManager**: Handles conversation persistence and validation
3. **Intent Detection**: Routes user input to appropriate handlers
4. **Command System**: Extensible command framework
5. **RAG Pipeline**: Retrieval, synthesis, and response generation

### Session Isolation
Each session maintains:
- Separate memory file (`.marketflow/memory/session_{id}.json`)
- Independent conversation history
- Session-specific system messages
- Isolated memory statistics

### Error Handling
- Graceful fallbacks for missing dependencies
- Informative error messages for users
- Logging of all errors for debugging
- Continue operation when possible

## Testing

Run the test suite to verify functionality:
```bash
python scripts/test_minimal_rag.py
```

Tests include:
- Session management functionality
- Intent detection and command routing
- Memory operations and persistence
- Chunk metadata handling
- Argument parsing

## Future Extensions

### MarketFlow API Integration
The intent detection system provides hooks for:
- Market data queries
- Technical analysis requests
- Trading signal generation
- Portfolio analysis

### Additional Commands
Easy to add new commands by extending the `detect_intent` method:
```python
elif user_input_lower.startswith('/analyze'):
    return {'type': 'command', 'action': 'market_analysis', 'params': ...}
```

### Enhanced RAG
- Multiple knowledge bases
- Hybrid search (keyword + semantic)
- Reranking and filtering
- Real-time data integration

## Configuration

The system respects MarketFlow configuration when available:
- Default LLM model from config
- Logging configuration
- Memory file locations
- API keys and settings

## Compatibility

This enhanced version maintains full backward compatibility with the original `minimal_rag.py` while adding significant new functionality for production use.