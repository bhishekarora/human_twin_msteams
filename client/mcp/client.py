import requests

query = input("Ask your question: ")
resp = requests.post("http://localhost:8000/query_meeting", json={"query": query})
print("Answer:", resp.json().get("response"))
