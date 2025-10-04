from typing import Dict, Tuple
from storage.csv_io import ensure_csv, read_all, atomic_replace
from storage.schemas import CHAR_HEADERS
from config import CHAR_CSV
from datetime import datetime, timedelta

def required_exp(level: int) -> int:
    # TODO(後で): config化して可変にする
    return 50 + 25 * level

def load_or_init(user_id: int) -> Dict:
    ensure_csv(CHAR_CSV, CHAR_HEADERS)
    rows = read_all(CHAR_CSV)
    for r in rows:
        if int(r.get("user_id", "1")) == user_id:
            return {
                "user_id": user_id,
                "level": int(r.get("level", "1")),
                "exp": int(r.get("exp", "0")),
                "streak": int(r.get("streak", "0")),
                "last_input_date": r.get("last_input_date", "")
            }
    rows.append({"user_id": str(user_id), "level": "1", "exp": "0", "streak": "0", "last_input_date": ""})
    atomic_replace(CHAR_CSV, rows, CHAR_HEADERS)
    return {"user_id": user_id, "level": 1, "exp": 0, "streak": 0, "last_input_date": ""}

def save(obj: Dict) -> None:
    rows = read_all(CHAR_CSV)
    for r in rows:
        if int(r.get("user_id", "1")) == obj["user_id"]:
            r.update({
                "level": str(obj["level"]),
                "exp": str(obj["exp"]),
                "streak": str(obj["streak"]),
                "last_input_date": obj["last_input_date"]
            })
            break
    else:
        rows.append({
            "user_id": str(obj["user_id"]),
            "level": str(obj["level"]),
            "exp": str(obj["exp"]),
            "streak": str(obj["streak"]),
            "last_input_date": obj["last_input_date"]
        })
    atomic_replace(CHAR_CSV, rows, CHAR_HEADERS)

def apply_entry_and_update(user_id: int, date_str: str) -> Tuple[Dict, int, bool]:
    st = load_or_init(user_id)
    gained = 500  # TODO(後で): config化
    leveled = False

    if st["last_input_date"]:
        last = datetime.strptime(st["last_input_date"], "%Y-%m-%d").date()
        today = datetime.strptime(date_str, "%Y-%m-%d").date()
        if today == last + timedelta(days=1):
            st["streak"] += 1
        elif today != last:
            st["streak"] = 1
        # 同日は据え置き
    else:
        st["streak"] = 1
    st["last_input_date"] = date_str

    st["exp"] += gained
    while st["exp"] >= required_exp(st["level"]):
        st["exp"] -= required_exp(st["level"])
        st["level"] += 1
        leveled = True

    save(st)
    return st, gained, leveled