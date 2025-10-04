# config.py
import os
import pathlib

# CSV の保存先ディレクトリ
# 本番(Render)では /var/data をマウント、ローカルは ./data を既定に
CSV_DIR = os.getenv("CSV_DIR", str(pathlib.Path("./data").resolve()))

# 個別ファイルパス（必要なら環境変数で上書き可）
ENTRIES_CSV = os.getenv("ENTRIES_CSV", os.path.join(CSV_DIR, "entries.csv"))
GOALS_CSV   = os.getenv("GOALS_CSV",   os.path.join(CSV_DIR, "monthly_goals.csv"))
CHAR_CSV    = os.getenv("CHAR_CSV",    os.path.join(CSV_DIR, "character_stats.csv"))

# 画像生成キー（未設定ならサーバ側はダミー応答）
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# CORS 許可ドメイン（カンマ区切り、未設定なら *）
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")