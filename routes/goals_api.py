# routes/goals_api.py
from flask import Blueprint, request, jsonify
import re
from domain.goals import get_goal, set_goal, sum_month_total

goals_bp = Blueprint("goals_bp", __name__)
valid_month = lambda m: bool(re.fullmatch(r"\d{4}-\d{2}", m))

@goals_bp.get("/goals/<month>")
def get_goals(month):
    if not valid_month(month):
        return {"error": "invalid month"}, 400

    user_id = int(request.args.get("user_id", "1"))
    result = sum_month_total(user_id, month)

    return jsonify({
        "month": month,
        "goal_amount": get_goal(user_id, month),
        "total": result["total"],
        "income_sum": result["income_sum"],
        "expense_sum": result["expense_sum"]
    }), 200


@goals_bp.put("/goals/<month>")
def put_goals(month):
    if not valid_month(month):
        return {"error": "invalid month"}, 400

    user_id = int(request.args.get("user_id", "1"))
    b = request.get_json(silent=True) or {}
    goal = int(b.get("goal_amount", -1))

    if goal < 0:
        return {"error": "goal_amount must be >= 0"}, 400

    set_goal(user_id, month, goal)
    return jsonify({
        "ok": True,
        "month": month,
        "goal_amount": goal
    }), 200
