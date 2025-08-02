"""
# web_interface.py
# This script provides a simple web interface for the MarketFlow LLM Query Engine.
# It allows users to submit queries and receive responses via a web browser.
# It uses Flask as the web framework and provides a simple HTML form for users to input queries.
"""

from flask import Flask, request, jsonify, render_template_string
# The query_llm import is no longer needed here.
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
import uuid

app = Flask(__name__)
# The engine is the core of the application; it should be the single source for responses.
engine = MarketflowLLMQueryEngine(enable_rag=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MarketFlow Query Engine</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .query-box { width: 100%; padding: 10px; margin: 10px 0; }
        .response { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; white-space: pre-wrap; } /* Added pre-wrap for better formatting */
        button { padding: 10px 20px; background: #007cba; color: white; border: none; border-radius: 5px; cursor: pointer; }
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
                // Corrected to handle Markdown-like newlines from the engine
                const formattedResponse = data.response.replace(/\\n/g, '<br>');
                // Updated to correctly display the query and the response from the server
                responseDiv.innerHTML = '<strong>Query:</strong> ' + query + '<br><br><strong>Response:</strong><br>' + formattedResponse;
            })
            .catch(error => {
                responseDiv.innerHTML = 'Error: ' + error;
            });
        };
    </script>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_query = data.get("query", "")
    session_id = data.get("session_id", "web-session-001")

    # The engine.process() method is designed to be the complete pipeline.
    # It already generates the final user-facing narrative.
    # Calling another LLM on its output was redundant and causing errors.
    engine_response = engine.process(user_query, session_id=session_id)

    # The JSON response must match what the frontend JavaScript expects.
    # The script expects a 'response' key.
    return jsonify({
        "response": engine_response
    })

if __name__ == '__main__':
    app.run(debug=True)