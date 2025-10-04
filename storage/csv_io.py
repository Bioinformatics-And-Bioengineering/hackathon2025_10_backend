import csv, os, tempfile
from typing import List, Dict

#役割: **「ファイルの初期化」**担当
def ensure_csv(path: str, headers: List[str]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)

#役割: **「全件読み込み」**担当
def read_all(path: str) -> List[Dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

#役割: **「追記」**担当
def append_row(path: str, row: Dict, headers: List[str]) -> None:
    # TODO(後で): ファイルロック導入（portalocker など）
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=headers).writerow(row)

#役割: **「安全な上書き保存」**担当
def atomic_replace(path: str, rows: List[Dict], headers: List[str]) -> None:
    d = os.path.dirname(path); os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_", suffix=".csv")
    os.close(fd)
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)

#役割: **「IDの自動採番」**担当
def next_id(path: str, id_field: str = "id") -> int:
    # TODO(後で): UUIDに切替 or counter.csv を atomic_update
    max_id = 0
    for r in read_all(path):
        try:
            max_id = max(max_id, int(r.get(id_field, 0)))
        except:
            pass
    return max_id + 1