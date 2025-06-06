from flask import Flask, request, jsonify
from rag_engine import load_and_ingest, search
import requests

app = Flask(__name__)
OLLAMA_API = "http://localhost:11434/api/generate"

# Load documents when the server starts
load_and_ingest("data")

@app.route("/query_meeting", methods=["POST"])
def query_meeting():
    query = request.json.get("query", "")
    top_chunks = search(query)
    context = "\n\n".join(top_chunks)
    
    prompt = f"Use the following meeting notes to answer the question:\n\n{context}\n\nQ: {query}\nA:"

    response = requests.post(OLLAMA_API, json={"model": "llama3", "prompt": prompt})
    answer = response.json().get("response", "No response from Ollama.")
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(port=8000)
