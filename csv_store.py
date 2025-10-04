import csv, os, fcntl
from datetime import datetime, timezone
from typing import List, Dict, Optional

HEADERS = ["id", "name", "content", "created_at", "ip"]

def _ensure_csv(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADERS)

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def read_entries(path: str, limit: int = 100) -> List[Dict]:
    _ensure_csv(path)
    rows: List[Dict] = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            for row in csv.DictReader(f):
                rows.append(row)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    rows.sort(key=lambda r: int(r["id"]), reverse=True)
    return rows[:limit]

def append_entry(path: str, name: str, content: str, ip: Optional[str] = None) -> int:
    _ensure_csv(path)
    with open(path, "r+", newline="", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.seek(0)
            last_id = 0
            for row in csv.DictReader(f):
                try:
                    last_id = max(last_id, int(row["id"]))
                except Exception:
                    pass
            new_id = last_id + 1
            f.seek(0, os.SEEK_END)
            csv.writer(f).writerow([str(new_id), name, content, _utc_now_iso(), ip or ""])
            return new_id
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
