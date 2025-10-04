from typing import List, Dict
from storage.csv_io import ensure_csv, read_all, append_row, next_id
from storage.schemas import ENTRIES_HEADERS
from config import ENTRIES_CSV

def list_by_month(user_id: int, month: str) -> List[Dict]:
    ensure_csv(ENTRIES_CSV, ENTRIES_HEADERS)
    rows = [
        r for r in read_all(ENTRIES_CSV)
        if int(r.get("user_id", "1")) == user_id and r.get("date", "").startswith(month)
    ]
    for r in rows:
        r["id"] = int(r["id"])
        r["user_id"] = int(r["user_id"])
        r["amount"] = int(r["amount"])
    rows.sort(key=lambda x: x["date"])
    return rows

def create_entry(user_id: int, date: str, category: str, amount: int, memo: str, type: str) -> Dict:
    # TODO(後で): type="income|expense" を受け取り、expense なら amount を負に
    ensure_csv(ENTRIES_CSV, ENTRIES_HEADERS)
    nid = next_id(ENTRIES_CSV)

    # 🔹 符号付け処理を追加
    if type == "expense":
        signed_amount = -abs(amount)
    elif type == "income":
        signed_amount = abs(amount)
    else:
        raise ValueError(f"Invalid type: {type}")
    
    row = {
        "id": str(nid),
        "user_id": str(user_id),
        "date": date,
        "category": category,
        "amount": str(signed_amount),
        "memo": memo
    }
    append_row(ENTRIES_CSV, row, ENTRIES_HEADERS)
    return {**row, "id": nid, "user_id": user_id, "amount": signed_amount}