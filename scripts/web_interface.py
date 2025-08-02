"""
# web_interface.py
# This script provides a simple web interface for the MarketFlow LLM Query Engine.
# It allows users to submit queries and receive responses via a web browser.
# It uses Flask as the web framework and provides a simple HTML form for users to input queries.
"""

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