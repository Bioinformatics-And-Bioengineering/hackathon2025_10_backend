# routes/state_api.py
from flask import Blueprint, request, jsonify
import re
from datetime import date
import calendar as cal
from domain.character import load_or_init
from domain.goals import get_goal, sum_month_total
from domain.entries import list_by_month

state_bp = Blueprint("state_bp", __name__)
valid_month = lambda m: bool(re.fullmatch(r"\d{4}-\d{2}", m))

@state_bp.get("/state")
def get_state():
    month = request.args.get("month")
    user_id = int(request.args.get("user_id", "1"))
    if not (month and valid_month(month)):
        return {"error":"month is required as YYYY-MM"}, 400

    character = load_or_init(user_id)
    goals = {"month": month,
             "goal_amount": get_goal(user_id, month),
             "total": sum_month_total(user_id, month)}

    y, m = map(int, month.split("-"))
    dim = cal.monthrange(y, m)[1]
    start_mon0 = date(y, m, 1).weekday()
    start_sun0 = (start_mon0 + 1) % 7

    per = {f"{month}-{str(d).zfill(2)}":{"total":0,"count":0} for d in range(1, dim+1)}
    entries = list_by_month(user_id, month)
    for r in entries:
        per[r["date"]]["total"] += r["amount"]
        per[r["date"]]["count"] += 1
    days = [{"date":k,"total":v["total"],"count":v["count"]} for k,v in per.items()]
    days.sort(key=lambda x:x["date"])

    calendar = {"month": month, "days_in_month": dim,
                "start_weekday_mon0": start_mon0, "start_weekday_sun0": start_sun0,
                "days": days}

    return jsonify({"character": character, "goals": goals,
                    "calendar": calendar, "entries": entries}), 200
