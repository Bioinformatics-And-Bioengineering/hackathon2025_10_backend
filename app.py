import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from csv_store import read_entries, append_entry

CSV_PATH = os.getenv("CSV_PATH", "/opt/backend/data/entries.csv")

app = Flask(__name__)
CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))

@app.get("/healthz")
def healthz():
    return {"ok": True}, 200

@app.get("/entries")
def list_entries():
    rows = read_entries(CSV_PATH, limit=100)
    return jsonify(rows), 200

@app.post("/entries")
def create_entry():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    content = (data.get("content") or "").strip()
    if not name or not content:
        return {"error": "name and content are required"}, 400
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    new_id = append_entry(CSV_PATH, name=name, content=content, ip=user_ip)
    return {"id": new_id}, 201

if __name__ == "__main__":
    app.run()

#aa