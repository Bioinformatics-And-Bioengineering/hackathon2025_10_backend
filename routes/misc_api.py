# routes/misc_api.py
from flask import Blueprint, request, jsonify, url_for
from datetime import date
import calendar as cal
from domain.character import load_or_init
from domain.entries import list_by_month
from . import level_to_tier  # ← ルートに置いた判定関数を使う

misc_bp = Blueprint("misc_bp", __name__)

@misc_bp.get("/character")
def get_character():
    user_id = int(request.args.get("user_id", "1"))
    ch = load_or_init(user_id)  # {user_id, level, exp, streak, last_input_date}

    # レベル→tier画像ファイル名を決定し、/static へのURLを作る
    filename = level_to_tier(ch["level"])  # 例: "tier3.png"
    image_url = url_for("static", filename=f"images/tiers/{filename}", _external=True)

    # 既存のフィールドに image_url を足して返す
    payload = {
        "user_id": ch["user_id"],
        "level": ch["level"],
        "exp": ch["exp"],
        "streak": ch["streak"],
        "last_input_date": ch["last_input_date"],
        "image_url": image_url,          # ★追加
        "image_tier_file": filename,     # （任意）どのtierかのデバッグ用
    }
    return jsonify(load_or_init(user_id)), 200

@misc_bp.get("/calendar/<month>")
def get_calendar(month):
    user_id = int(request.args.get("user_id", "1"))
    y, m = map(int, month.split("-"))
    dim = cal.monthrange(y, m)[1]
    start_mon0 = date(y, m, 1).weekday()
    start_sun0 = (start_mon0 + 1) % 7

    per = {f"{month}-{str(d).zfill(2)}":{"total":0,"count":0} for d in range(1, dim+1)}
    for r in list_by_month(user_id, month):
        per[r["date"]]["total"] += r["amount"]
        per[r["date"]]["count"] += 1

    days = [{"date":k,"total":v["total"],"count":v["count"]} for k,v in per.items()]
    days.sort(key=lambda x:x["date"])
    return jsonify({
        "month": month,
        "days_in_month": dim,
        "start_weekday_mon0": start_mon0,
        "start_weekday_sun0": start_sun0,
        "days": days
    }), 200
