# MarketFlow LLM Query Engine - Local Deployment Guide

## 🚀 Complete Setup and Deployment Instructions

This comprehensive guide will help you deploy and run the enhanced MarketFlow LLM Query Engine on your local environment.

---

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Repository Setup](#-repository-setup)
3. [Environment Configuration](#-environment-configuration)
4. [Dependency Installation](#-dependency-installation)
5. [API Keys Configuration](#-api-keys-configuration)
6. [Testing the Installation](#-testing-the-installation)
7. [Running the Query Engine](#-running-the-query-engine)
8. [Advanced Configuration](#-advanced configuration)
9. [Troubleshooting](#-troubleshooting)
10. [Performance Optimization](#-performance-optimization)

---

## 📋 Prerequisites

### System Requirements

**Operating System:**

- Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- 64-bit architecture required

**Hardware Requirements:**

- **RAM:** Minimum 8GB, Recommended 16GB+
- **Storage:** At least 5GB free space
- **CPU:** Multi-core processor (4+ cores recommended)
- **Network:** Stable internet connection for API access

### Software Requirements

**Python Environment:**

- **Python 3.8+** (Python 3.11 recommended)
- **pip** package manager
- **Virtual environment** capability (venv, conda, or virtualenv)

**Git:**

- Git version control system installed
- GitHub account access (for repository cloning)

**Optional but Recommended:**

- **VS Code** or similar IDE for code editing
- **Docker** (for containerized deployment)
- **Conda** for advanced environment management

### Knowledge Prerequisites

**Basic Understanding Of:**

- Command line/terminal usage
- Python package management
- Environment variables
- API key management
- Basic Git operations

---

## 🔄 Repository Setup

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
# Clone the MarketFlow repository
git clone https://github.com/Martinolli/marketflow.git

# Navigate to the project directory
cd marketflow

# Verify the repository structure
ls -la
```

**Expected Directory Structure:**

```btach
marketflow/
├── marketflow/                 # Main package directory
│   ├── marketflow_llm_query_engine.py  # Enhanced query engine
│   ├── marketflow_llm_interface.py     # LLM interface
│   ├── marketflow_facade.py            # Analysis facade
│   ├── concepts/                       # VPA/Wyckoff concepts
│   └── ...
├── rag/                        # RAG system components
├── tests/                      # Test suites
├── scripts/                    # Utility scripts
├── knowledgebase/             # Knowledge base files
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── DEPLOYMENT_GUIDE.md        # This guide
```

### Step 2: Verify Repository Integrity

```bash
# Check the latest commit
git log --oneline -5

# Verify important files exist
ls marketflow/marketflow_llm_query_engine.py
ls marketflow/concepts/vpa_concepts.yaml
ls marketflow/concepts/wyckoff_concepts.yaml
ls rag/retriever.py
```

### Step 3: Create Project Backup (Optional but Recommended)

```bash
# Create a backup of the original repository
cp -r marketflow marketflow_backup

# Or create a new branch for your customizations
cd marketflow
git checkout -b local-deployment
```

---

## 🔧 Environment Configuration

### Step 1: Create Python Virtual Environment

**Using venv (Recommended):**

```bash
# Create virtual environment
python -m venv marketflow_env

# Activate virtual environment
# On Windows:
marketflow_env\Scripts\activate
# On macOS/Linux:
source marketflow_env/bin/activate

# Verify activation (should show virtual environment name)
which python
python --version
```

**Using conda (Alternative):**

```bash
# Create conda environment
conda create -n marketflow python=3.11

# Activate conda environment
conda activate marketflow

# Verify activation
python --version
```

### Step 2: Upgrade pip and Essential Tools

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install essential build tools
pip install wheel setuptools

# Verify pip version
pip --version
```

### Step 3: Set Python Path

**For Current Session:**

```bash
# On Windows:
set PYTHONPATH=%CD%

# On macOS/Linux:
export PYTHONPATH=$(pwd)
```

**For Permanent Setup (Optional):**

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env

# Add Python path (adjust path as needed)
echo "PYTHONPATH=/path/to/your/marketflow" >> .env
```

---

## 📦 Dependency Installation

### Step 1: Install Core Dependencies

```bash
# Install all required packages from requirements.txt
pip install -r requirements.txt

# If requirements.txt is missing or incomplete, install manually:
pip install python-dotenv
pip install chromadb
pip install openai
pip install polygon-api-client
pip install pyyaml
pip install tenacity
pip install numpy
pip install pandas
pip install matplotlib
pip install seaborn
pip install plotly
```

### Step 2: Install Additional Dependencies

**For Enhanced Functionality:**

```bash
# Data analysis and visualization
pip install scipy
pip install scikit-learn
pip install jupyter

# Web framework (if using web interface)
pip install flask
pip install flask-cors

# Development tools
pip install pytest
pip install black
pip install flake8
```

### Step 3: Verify Installation

```bash
# Test import of key modules
python -c "import openai; print('OpenAI: OK')"
python -c "import chromadb; print('ChromaDB: OK')"
python -c "import yaml; print('YAML: OK')"
python -c "import pandas; print('Pandas: OK')"
python -c "from polygon import RESTClient; print('Polygon: OK')"

# Test MarketFlow imports
python -c "from marketflow.enums import QueryIntent; print('MarketFlow Enums: OK')"
```

### Step 4: Handle Common Installation Issues

**ChromaDB Installation Issues:**

```bash
# If ChromaDB fails to install
pip install --upgrade pip setuptools wheel
pip install chromadb --no-cache-dir

# Alternative: Install specific version
pip install chromadb==0.4.15
```

**OpenAI Installation Issues:**

```bash
# Install specific OpenAI version
pip install openai==1.3.0

# Or latest version
pip install --upgrade openai
```

**Polygon API Issues:**

```bash
# Install polygon-api-client
pip install polygon-api-client

# Verify installation
python -c "from polygon import RESTClient; print('Polygon API client installed successfully')"
```

---

## 🔑 API Keys Configuration

### Step 1: Obtain Required API Keys

**OpenAI API Key (Required for RAG functionality):**

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new secret key
5. Copy the key (starts with `sk-`)

**Polygon.io API Key (Required for market data):**

1. Visit [Polygon.io](https://polygon.io/)
2. Sign up for a free or paid account
3. Navigate to your dashboard
4. Copy your API key

### Step 2: Configure Environment Variables

#### Method 1: Using .env File (Recommended)

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your API keys to the `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# Polygon.io Configuration
POLYGON_API_KEY=your-polygon-api-key-here

# Optional: Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=marketflow.log

# Optional: RAG Configuration
ENABLE_RAG=true
RAG_TOP_K=5
```

#### Method 2: System Environment Variables

**On Windows:**

```cmd
set OPENAI_API_KEY=sk-your-openai-api-key-here
set OPENAI_API_BASE=https://api.openai.com/v1
set POLYGON_API_KEY=your-polygon-api-key-here
```

**On macOS/Linux:**

```bash
export OPENAI_API_KEY=sk-your-openai-api-key-here
export OPENAI_API_BASE=https://api.openai.com/v1
export POLYGON_API_KEY=your-polygon-api-key-here
```

### Step 3: Verify API Key Configuration

```bash
# Test OpenAI API key
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('OpenAI API Key:', os.getenv('OPENAI_API_KEY', 'NOT SET')[:10] + '...')
print('Polygon API Key:', os.getenv('POLYGON_API_KEY', 'NOT SET')[:10] + '...')
"
```

### Step 4: Security Best Practices

**Protect Your API Keys:**

```bash
# Add .env to .gitignore to prevent accidental commits
echo ".env" >> .gitignore
echo "*.env" >> .gitignore

# Set appropriate file permissions (Unix/Linux/macOS)
chmod 600 .env
```

**API Key Usage Limits:**

- Monitor your OpenAI usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- Set up billing alerts to avoid unexpected charges
- Use Polygon.io free tier limits wisely (5 API calls/minute)

---

## 🧪 Testing the Installation

### Step 1: Run Basic System Tests

```bash
# Run the enhanced query engine test suite
python tests/test_enhanced_query_engine.py

# Expected output should show:
# ✅ Input Validation: PASSED
# ✅ Intent Parsing: PASSED  
# ✅ Ticker Extraction: PASSED
```

### Step 2: Run Integration Tests

```bash
# Run complete integration tests
python tests/test_complete_integration.py

# Expected output should show:
# ✅ Query Processing: PASSED
# ✅ Conversation Flow: PASSED
# ✅ Error Handling Robustness: PASSED
# ✅ System Integration: PASSED
```

### Step 3: Run Enhanced RAG Tests

```bash
# Test the enhanced RAG functionality
python tests/test_enhanced_rag.py

# Expected output should show:
# ✅ RAG Fallback Mechanisms: PASSED
# ✅ Local Concept Search: PASSED
# ✅ Keyword Search Intelligence: PASSED
# ✅ RAG Integration with Queries: PASSED
# ✅ RAG Performance: PASSED
```

### Step 4: Test Real Market Data (Optional)

```bash
# Test with real market data (requires API keys)
python tests/test_real_market_data.py

# This test will show how the system handles:
# - Real ticker analysis
# - Comparison analysis
# - Portfolio analysis
# - Concept integration
# - System limitations
```

### Step 5: Manual Functionality Test

Create a simple test script to verify basic functionality:

```python
# Create test_manual.py
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

# Initialize the query engine
engine = MarketflowLLMQueryEngine(enable_rag=True)

# Test basic queries
test_queries = [
    "What is accumulation?",
    "Analyze AAPL", 
    "Compare AAPL and MSFT",
    "What does Anna Coulling say about volume?"
]

for query in test_queries:
    print(f"\nQuery: {query}")
    response = engine.process(query, session_id="test_session")
    print(f"Response: {response[:200]}...")
```

Run the manual test:

```bash
python test_manual.py
```

### Step 6: Troubleshoot Common Issues

**If tests fail with import errors:**

```bash
# Ensure PYTHONPATH is set correctly
export PYTHONPATH=$(pwd)  # On Unix/Linux/macOS
set PYTHONPATH=%CD%       # On Windows

# Re-run the tests
python tests/test_enhanced_query_engine.py
```

**If API-related tests fail:**

- Verify your API keys are correctly set in `.env`
- Check your internet connection
- Verify API key permissions and quotas
- The system should gracefully handle API failures with fallback responses

---

## 🚀 Running the Query Engine

### Method 1: Interactive Python Session

```python
# Start Python interpreter
python

# Import and initialize the query engine
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

# Create query engine instance
engine = MarketflowLLMQueryEngine(enable_rag=True)

# Process queries
response = engine.process("What is accumulation?", session_id="my_session")
print(response)

# Continue with more queries
response = engine.process("Analyze AAPL", session_id="my_session")
print(response)
```

### Method 2: Command Line Interface

The query engine includes a built-in CLI for easy testing:

```bash
# Run the CLI interface
python -c "
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
engine = MarketflowLLMQueryEngine(enable_rag=True)

# Interactive mode
while True:
    query = input('MarketFlow> ')
    if query.lower() in ['exit', 'quit']:
        break
    response = engine.process(query, session_id='cli_session')
    print(f'Response: {response}\n')
"
```

### Method 3: Script-Based Usage

Create a custom script for your specific use cases:

```python
# Create run_marketflow.py
#!/usr/bin/env python3
import sys
import os
from datetime import datetime

# Add project to path
sys.path.insert(0, os.path.abspath('.'))

from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

def main():
    print("MarketFlow LLM Query Engine")
    print("=" * 40)
    
    # Initialize engine
    engine = MarketflowLLMQueryEngine(enable_rag=True)
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Example queries
    queries = [
        "What is VPA?",
        "Analyze NVDA",
        "Compare AAPL and MSFT",
        "What is accumulation?",
        "Show me Wyckoff concepts"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: {query}")
        response = engine.process(query, session_id=session_id)
        print(f"📝 Response: {response}")
        print("-" * 60)

if __name__ == "__main__":
    main()
```

Run your custom script:

```bash
python run_marketflow.py
```

### Method 4: Web Interface (Advanced)

Create a simple Flask web interface:

```python
# Create web_interface.py
from flask import Flask, request, jsonify, render_template_string
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
import uuid

app = Flask(__name__)
engine = MarketflowLLMQueryEngine(enable_rag=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MarketFlow Query Engine</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .query-box { width: 100%; padding: 10px; margin: 10px 0; }
        .response { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        button { padding: 10px 20px; background: #007cba; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>MarketFlow LLM Query Engine</h1>
    <form id="queryForm">
        <input type="text" id="query" class="query-box" placeholder="Enter your query (e.g., 'What is accumulation?', 'Analyze AAPL')" />
        <br>
        <button type="submit">Submit Query</button>
    </form>
    <div id="response" class="response" style="display:none;"></div>
    
    <script>
        document.getElementById('queryForm').onsubmit = function(e) {
            e.preventDefault();
            const query = document.getElementById('query').value;
            const responseDiv = document.getElementById('response');
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = 'Processing...';
            
            fetch('/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: query})
            })
            .then(response => response.json())
            .then(data => {
                responseDiv.innerHTML = '<strong>Query:</strong> ' + query + '<br><br><strong>Response:</strong> ' + data.response;
            })
            .catch(error => {
                responseDiv.innerHTML = 'Error: ' + error;
            });
        };
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_text = data.get('query', '')
    session_id = str(uuid.uuid4())
    
    try:
        response = engine.process(query_text, session_id=session_id)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Run the web interface:

```bash
# Install Flask if not already installed
pip install flask flask-cors

# Run the web interface
python web_interface.py

# Open browser to http://localhost:5000
```

### Method 5: Jupyter Notebook Integration

Create a Jupyter notebook for interactive analysis:

```python
# In Jupyter notebook cell
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
import pandas as pd

# Initialize engine
engine = MarketflowLLMQueryEngine(enable_rag=True)

# Create interactive widget
from IPython.widgets import interact, widgets

@interact(query=widgets.Text(value="What is accumulation?", description="Query:"))
def query_marketflow(query):
    response = engine.process(query, session_id="jupyter_session")
    print(f"Response: {response}")
```

---

## ⚙️ Advanced Configuration

### Query Engine Configuration Options

The MarketflowLLMQueryEngine supports various configuration options:

```python
# Advanced initialization with custom parameters
engine = MarketflowLLMQueryEngine(
    enable_rag=True,                    # Enable RAG functionality
    rag_top_k=5,                       # Number of RAG results to retrieve
    max_context_length=10,             # Maximum conversation context length
    enable_logging=True,               # Enable detailed logging
    log_level="INFO",                  # Logging level (DEBUG, INFO, WARNING, ERROR)
    session_timeout=3600,              # Session timeout in seconds
    enable_caching=True,               # Enable response caching
    cache_size=100                     # Maximum cache entries
)
```

### Logging Configuration

**Configure detailed logging for debugging:**

```python
import logging
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('marketflow_debug.log'),
        logging.StreamHandler()
    ]
)

# Initialize with logging enabled
engine = MarketflowLLMQueryEngine(enable_rag=True, log_level="DEBUG")
```

### RAG System Configuration

**Customize RAG behavior:**

```python
# Configure RAG system parameters
engine = MarketflowLLMQueryEngine(
    enable_rag=True,
    rag_top_k=10,                      # Retrieve more results
    rag_similarity_threshold=0.7,      # Minimum similarity score
    enable_local_fallback=True,        # Enable local concept fallback
    enable_keyword_search=True         # Enable keyword-based search
)
```

### Performance Optimization

**Memory Management:**

```python
# For memory-constrained environments
engine = MarketflowLLMQueryEngine(
    enable_rag=True,
    max_context_length=5,              # Reduce context window
    cache_size=50,                     # Smaller cache
    enable_gc=True                     # Enable garbage collection
)
```

**Response Time Optimization:**

```python
# For faster responses
engine = MarketflowLLMQueryEngine(
    enable_rag=False,                  # Disable RAG for speed
    enable_caching=True,               # Enable aggressive caching
    timeout=5                          # Set response timeout
)
```

### Custom Concept Integration

**Add your own concepts:**

```python
# Create custom concepts YAML file
custom_concepts = {
    'my_custom_concept': {
        'explanation': 'My custom trading concept explanation',
        'category': 'custom',
        'examples': ['Example 1', 'Example 2']
    }
}

# Save to YAML file
import yaml
with open('marketflow/concepts/custom_concepts.yaml', 'w') as f:
    yaml.dump(custom_concepts, f)

# The engine will automatically load custom concepts
```

### Multi-Language Support (Future Enhancement)

**Prepare for multi-language support:**

```python
# Configure language settings
engine = MarketflowLLMQueryEngine(
    enable_rag=True,
    language='en',                     # Default language
    enable_translation=False,          # Future feature
    fallback_language='en'             # Fallback language
)
```

### Integration with External Systems

**Database Integration:**

```python
# Example: Log queries to database
import sqlite3

class DatabaseLogger:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()
    
    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                session_id TEXT,
                query TEXT,
                response TEXT,
                intent TEXT,
                confidence REAL
            )
        ''')
    
    def log_query(self, session_id, query, response, intent, confidence):
        from datetime import datetime
        self.conn.execute('''
            INSERT INTO query_log (timestamp, session_id, query, response, intent, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), session_id, query, response, intent, confidence))
        self.conn.commit()

# Use with query engine
db_logger = DatabaseLogger('marketflow_queries.db')

# Custom wrapper to log queries
def process_with_logging(engine, query, session_id):
    response = engine.process(query, session_id)
    # Log to database (implement intent/confidence extraction)
    db_logger.log_query(session_id, query, response, "unknown", 0.0)
    return response
```

### Docker Deployment

**Create Dockerfile:**

```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Expose port for web interface
EXPOSE 5000

# Run the application
CMD ["python", "web_interface.py"]
```

**Build and run Docker container:**

```bash
# Build Docker image
docker build -t marketflow-query-engine .

# Run container with environment variables
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=your-key-here \
  -e POLYGON_API_KEY=your-key-here \
  marketflow-query-engine
```

---

## 🔧 Troubleshooting

### Common Installation Issues

#### Issue: ModuleNotFoundError: No module named 'marketflow'

```bash
# Solution: Set PYTHONPATH correctly
export PYTHONPATH=$(pwd)  # Unix/Linux/macOS
set PYTHONPATH=%CD%       # Windows

# Or install in development mode
pip install -e .
```

#### Issue: ChromaDB installation fails

```bash
# Solution: Install with specific version
pip install chromadb==0.4.15 --no-cache-dir

# Or use conda
conda install -c conda-forge chromadb
```

#### Issue: OpenAI API errors**

```bash
# Check API key format
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print('Key format correct:', key.startswith('sk-') if key else 'NOT SET')
"

# Test API connection
python -c "
import openai
import os
from dotenv import load_dotenv
load_dotenv()
client = openai.OpenAI()
try:
    response = client.models.list()
    print('OpenAI API connection: OK')
except Exception as e:
    print(f'OpenAI API error: {e}')
"
```

### Runtime Issues

#### Issue: Slow response times

```python
# Solution: Disable RAG for faster responses
engine = MarketflowLLMQueryEngine(enable_rag=False)

# Or reduce RAG results
engine = MarketflowLLMQueryEngine(enable_rag=True, rag_top_k=3)
```

#### Issue: Memory usage too high

```python
# Solution: Reduce context window and cache size
engine = MarketflowLLMQueryEngine(
    max_context_length=3,
    cache_size=20,
    enable_gc=True
)
```

#### Issue: API rate limits exceeded

```bash
# Solution: Implement rate limiting
import time

def rate_limited_query(engine, query, session_id, delay=1):
    response = engine.process(query, session_id)
    time.sleep(delay)  # Add delay between requests
    return response
```

### API-Related Issues

#### Issue: Polygon API rate limits

```python
# Solution: Implement exponential backoff
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
```

#### Issue: OpenAI API quota exceeded

```python
# Solution: Use local fallbacks
engine = MarketflowLLMQueryEngine(
    enable_rag=True,
    enable_local_fallback=True,  # Always use local concepts first
    rag_timeout=5                # Quick timeout for API calls
)
```

### Data-Related Issues

#### Issue: Concept files not loading

```bash
# Check YAML file integrity
python -c "
import yaml
try:
    with open('marketflow/concepts/vpa_concepts.yaml', 'r') as f:
        data = yaml.safe_load(f)
    print('VPA concepts loaded:', len(data))
except Exception as e:
    print('VPA concepts error:', e)
"
```

#### Issue: RAG database corruption

```bash
# Solution: Rebuild ChromaDB
rm -rf rag/chroma_db/  # Remove existing database
python rag/chunker.py  # Rebuild database
```

### Performance Debugging

**Enable detailed performance logging:**

```python
import logging
import time

class PerformanceLogger:
    def __init__(self):
        self.logger = logging.getLogger('performance')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - PERF - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def time_function(self, func, *args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        self.logger.debug(f'{func.__name__} took {end_time - start_time:.2f}s')
        return result

# Use performance logger
perf_logger = PerformanceLogger()
response = perf_logger.time_function(engine.process, "Analyze AAPL", "test_session")
```

### Environment-Specific Issues

**Windows-Specific Issues:**

```cmd
# Path separator issues
set PYTHONPATH=%CD%

# Long path issues
git config --system core.longpaths true
```

**macOS-Specific Issues:**

```bash
# Permission issues
sudo chown -R $(whoami) /usr/local/lib/python3.11/site-packages/

# SSL certificate issues
/Applications/Python\ 3.11/Install\ Certificates.command
```

**Linux-Specific Issues:**

```bash
# Missing system dependencies
sudo apt-get update
sudo apt-get install python3-dev build-essential

# Permission issues
sudo chown -R $USER:$USER ~/.local/
```

### Getting Help

**Debug Information Collection:**

```python
# Create debug_info.py
import sys
import os
import platform
from datetime import datetime

def collect_debug_info():
    info = {
        'timestamp': datetime.now().isoformat(),
        'platform': platform.platform(),
        'python_version': sys.version,
        'python_path': sys.path,
        'environment_variables': {
            'PYTHONPATH': os.getenv('PYTHONPATH'),
            'OPENAI_API_KEY': 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET',
            'POLYGON_API_KEY': 'SET' if os.getenv('POLYGON_API_KEY') else 'NOT SET'
        }
    }
    
    # Test imports
    try:
        from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
        info['marketflow_import'] = 'OK'
    except Exception as e:
        info['marketflow_import'] = f'ERROR: {e}'
    
    return info

if __name__ == "__main__":
    debug_info = collect_debug_info()
    for key, value in debug_info.items():
        print(f"{key}: {value}")
```

Run debug info collection:

```bash
python debug_info.py > debug_report.txt
```

**Community Support:**

- Create GitHub issues with debug information
- Include error logs and system information
- Provide minimal reproducible examples

---

## ⚡ Performance Optimization

### Response Time Optimization

**1. Disable RAG for Speed:**

```python
# For fastest responses, disable RAG
engine = MarketflowLLMQueryEngine(enable_rag=False)
# Expected response time: < 1 second
```

**2. Optimize RAG Settings:**

```python
# Balance between speed and accuracy
engine = MarketflowLLMQueryEngine(
    enable_rag=True,
    rag_top_k=3,                    # Reduce from default 5
    rag_timeout=3,                  # Quick timeout
    enable_local_fallback=True      # Fast local fallback
)
# Expected response time: 2-5 seconds
```

**3. Enable Caching:**

```python
# Cache frequent queries
engine = MarketflowLLMQueryEngine(
    enable_caching=True,
    cache_size=200,                 # Increase cache size
    cache_ttl=3600                  # 1 hour cache lifetime
)
```

### Memory Optimization

**1. Reduce Context Window:**

```python
# For memory-constrained environments
engine = MarketflowLLMQueryEngine(
    max_context_length=3,           # Reduce from default 10
    enable_gc=True                  # Enable garbage collection
)
```

**2. Batch Processing:**

```python
# Process multiple queries efficiently
def batch_process(engine, queries, session_id):
    results = []
    for query in queries:
        result = engine.process(query, session_id)
        results.append(result)
        # Optional: Clear cache periodically
        if len(results) % 10 == 0:
            engine.clear_cache()
    return results
```

### Production Deployment Optimization

**1. Use Process Pool for Concurrent Requests:**

```python
from multiprocessing import Pool
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

def process_query(args):
    query, session_id = args
    engine = MarketflowLLMQueryEngine(enable_rag=True)
    return engine.process(query, session_id)

# Handle multiple concurrent requests
def handle_concurrent_queries(queries_and_sessions):
    with Pool(processes=4) as pool:
        results = pool.map(process_query, queries_and_sessions)
    return results
```

**2. Implement Connection Pooling:**

```python
# For database connections and API clients
import threading
from queue import Queue

class EnginePool:
    def __init__(self, pool_size=5):
        self.pool = Queue(maxsize=pool_size)
        for _ in range(pool_size):
            engine = MarketflowLLMQueryEngine(enable_rag=True)
            self.pool.put(engine)
    
    def get_engine(self):
        return self.pool.get()
    
    def return_engine(self, engine):
        self.pool.put(engine)
    
    def process_query(self, query, session_id):
        engine = self.get_engine()
        try:
            result = engine.process(query, session_id)
            return result
        finally:
            self.return_engine(engine)
```

### Monitoring and Metrics

**1. Performance Monitoring:**

```python
import time
import statistics
from collections import defaultdict

class PerformanceMonitor:
    def __init__(self):
        self.response_times = []
        self.query_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
    
    def log_query(self, query, response_time, success=True):
        self.response_times.append(response_time)
        self.query_counts[query] += 1
        if not success:
            self.error_counts[query] += 1
    
    def get_stats(self):
        if not self.response_times:
            return {}
        
        return {
            'avg_response_time': statistics.mean(self.response_times),
            'median_response_time': statistics.median(self.response_times),
            'max_response_time': max(self.response_times),
            'min_response_time': min(self.response_times),
            'total_queries': len(self.response_times),
            'error_rate': sum(self.error_counts.values()) / len(self.response_times)
        }

# Usage
monitor = PerformanceMonitor()

def monitored_process(engine, query, session_id):
    start_time = time.time()
    try:
        response = engine.process(query, session_id)
        success = True
    except Exception as e:
        response = f"Error: {e}"
        success = False
    
    response_time = time.time() - start_time
    monitor.log_query(query, response_time, success)
    return response
```

---

## 🎯 Quick Start Summary

### Minimal Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/Martinolli/marketflow.git
cd marketflow

# 2. Create virtual environment
python -m venv marketflow_env
source marketflow_env/bin/activate  # Unix/Linux/macOS
# marketflow_env\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set Python path
export PYTHONPATH=$(pwd)  # Unix/Linux/macOS
# set PYTHONPATH=%CD%     # Windows

# 5. Test installation
python tests/test_enhanced_query_engine.py
```

### Basic Usage

```python
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

# Initialize (works without API keys for basic functionality)
engine = MarketflowLLMQueryEngine(enable_rag=False)

# Process queries
response = engine.process("What is accumulation?", session_id="test")
print(response)
```

### With API Keys (Full Functionality)

```bash
# Create .env file with your API keys
echo "OPENAI_API_KEY=sk-your-key-here" > .env
echo "POLYGON_API_KEY=your-polygon-key" >> .env

# Enable full RAG functionality
python -c "
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
engine = MarketflowLLMQueryEngine(enable_rag=True)
response = engine.process('What does Anna Coulling say about volume?', 'test')
print(response)
"
```

---

## 📚 Additional Resources

### Documentation

- **README.md**: Project overview and basic usage
- **CHANGELOG.md**: Version history and updates
- **API Documentation**: In-code docstrings and type hints

### Example Scripts

- **tests/test_enhanced_query_engine.py**: Comprehensive test suite
- **tests/test_real_market_data.py**: Real-world usage examples
- **scripts/**: Utility scripts for various tasks

### Community and Support

- **GitHub Repository**: `https://github.com/Martinolli/marketflow`
- **Issues**: Report bugs and request features
- **Discussions**: Community support and questions

### Related Projects

- **VPA Modular Package**: Core VPA analysis components
- **Wyckoff Method Resources**: Educational materials and concepts

---

## 🎉 Conclusion

You now have a complete, production-ready MarketFlow LLM Query Engine deployment! The system provides:

✅ **10 Query Types** - Comprehensive analysis capabilities  
✅ **Enhanced RAG System** - Multi-level fallback mechanisms  
✅ **Robust Error Handling** - Graceful degradation and recovery  
✅ **Local Concept Access** - Instant responses without API dependency  
✅ **Production Ready** - Tested, optimized, and documented  

### Next Steps

1. **Customize** the system for your specific trading strategies
2. **Integrate** with your existing trading tools and workflows  
3. **Extend** functionality with additional query types or data sources
4. **Scale** the deployment for production use with multiple users
5. **Contribute** improvements back to the community

### Support

If you encounter any issues or need assistance:

1. Check the **Troubleshooting** section above
2. Run the **debug_info.py** script to collect system information
3. Create a GitHub issue with detailed information
4. Join the community discussions for peer support

#### Happy Trading with MarketFlow! 📈

---

*Last updated: August 2025*  
*Version: Enhanced Query Engine v2.0*
