from typing import Optional
from storage.csv_io import ensure_csv, read_all, atomic_replace
from storage.schemas import GOALS_HEADERS, ENTRIES_HEADERS
from config import GOALS_CSV, ENTRIES_CSV

def get_goal(user_id: int, month: str) -> Optional[int]:
    ensure_csv(GOALS_CSV, GOALS_HEADERS)
    for r in read_all(GOALS_CSV):
        if int(r.get("user_id", "1")) == user_id and r.get("month") == month:
            try:
                return int(r.get("goal_amount", "0"))
            except:
                return 0
    return None

def set_goal(user_id: int, month: str, goal: int) -> None:
    ensure_csv(GOALS_CSV, GOALS_HEADERS)
    rows = read_all(GOALS_CSV)
    for r in rows:
        if int(r.get("user_id", "1")) == user_id and r.get("month") == month:
            r["goal_amount"] = str(goal)
            break
    else:
        rows.append({"user_id": str(user_id), "month": month, "goal_amount": str(goal)})
    atomic_replace(GOALS_CSV, rows, GOALS_HEADERS)

def sum_month_total(user_id: int, month: str):
    ensure_csv(ENTRIES_CSV, ENTRIES_HEADERS)
    income_sum = 0
    expense_sum = 0

    for r in read_all(ENTRIES_CSV):
        if int(r.get("user_id", "1")) == user_id and r.get("date", "").startswith(month):
            try:
                amount = int(r.get("amount", "0"))
                # amountが正のとき収入、負のとき支出として扱う
                if amount >= 0:
                    income_sum += amount
                else:
                    expense_sum += abs(amount)
            except:
                pass

    total = income_sum - expense_sum
    return {"total": total, "income_sum": income_sum, "expense_sum": expense_sum}
