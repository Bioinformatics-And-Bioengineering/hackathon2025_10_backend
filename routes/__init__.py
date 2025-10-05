# routes/__init__.py
# パッケージ化のための空ファイル
def level_to_tier(level: int) -> str:
    # 例: レベル帯を4分割
    if level <= 2:
        return "tier1.png"
    elif level <= 5:
        return "tier2.png"
    elif level <= 8:
        return "tier3.png"
    else:
        return "tier4.png"