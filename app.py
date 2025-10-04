import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from csv_store import read_entries, append_entry

# Render ではディスクを /var/data にマウントする想定（render.yamlで設定）
CSV_PATH = os.getenv("CSV_PATH", "/var/data/entries.csv")

app = Flask(__name__)
CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))

@app.get("/healthz")
def healthz():
    return {"日付": 2025}, 200

@app.get("/healthz2")
def healthz2():
    return {"日付": 20251004}, 200

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
    import os
    port = int(os.getenv("PORT", "5000"))  # ← Render が割り当てるポートを使用
    app.run(host="0.0.0.0", port=port)     # 本番では debug=False 推奨
