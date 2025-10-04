# routes/entries_api.py
from flask import Blueprint, request, jsonify
import re
from domain.entries import list_by_month, create_entry
from domain.character import apply_entry_and_update

entries_bp = Blueprint("entries_bp", __name__)

valid_month = lambda m: bool(re.fullmatch(r"\d{4}-\d{2}", m))
valid_date  = lambda d: bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", d))

@entries_bp.get("/entries")
def get_entries():
    month = request.args.get("month")
    user_id = int(request.args.get("user_id", "1"))
    if not (month and valid_month(month)):
        return {"error": "month is required as YYYY-MM"}, 400
    return jsonify({"entries": list_by_month(user_id, month)}), 200

@entries_bp.post("/entries")
def post_entry():
    b = request.get_json(silent=True) or {}
    try:
        user_id = int(b.get("user_id", 1))
        date    = (b.get("date") or "").strip()
        category= (b.get("category") or "").strip()
        amount  = int(b.get("amount", -1))  # デモ中は正の値で受ける
        memo    = (b.get("memo") or "").strip()

        if not (valid_date(date) and category and amount >= 0):
            return {"error": "invalid payload"}, 400

        entry = create_entry(user_id, date, category, amount, memo)
        ch, gained, leveled = apply_entry_and_update(user_id, date)

        return jsonify({
            "entry": entry,
            "character": {
                "level": ch["level"], "exp": ch["exp"],
                "expGained": gained, "streak": ch["streak"],
                "leveledUp": leveled
            }
        }), 201
    except Exception as e:
        return {"error": str(e)}, 500
