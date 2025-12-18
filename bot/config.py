from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Загружаем .env как можно раньше
load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing in environment (.env)")

_admin_raw = os.getenv("ADMIN_TG_ID", "").strip()
if not _admin_raw:
    raise RuntimeError("ADMIN_TG_ID is missing in environment (.env)")
try:
    ADMIN_TG_ID: int = int(_admin_raw)
except ValueError as e:
    raise RuntimeError("ADMIN_TG_ID must be an integer") from e

_db_raw = os.getenv("DB_PATH", "data/bot.db").strip() or "data/bot.db"
DB_PATH: Path = Path(_db_raw)
