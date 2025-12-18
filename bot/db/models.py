from __future__ import annotations

LEADS_TABLE = "leads"
LEAD_FILES_TABLE = "lead_files"

LEADS_COLUMNS: tuple[str, ...] = (
    "id",
    "created_at",
    "tg_user_id",
    "tg_username",
    "tg_full_name",
    "service",
    "task",
    "deadline",
    "budget",
    "contact",
    "extra_json",
)

LEAD_FILES_COLUMNS: tuple[str, ...] = (
    "id",
    "lead_id",
    "file_type",
    "file_id",
)

CREATE_TABLE_LEADS_SQL = f"""
CREATE TABLE IF NOT EXISTS {LEADS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    tg_user_id INTEGER NOT NULL,
    tg_username TEXT,
    tg_full_name TEXT NOT NULL,
    service TEXT NOT NULL,
    task TEXT NOT NULL,
    deadline TEXT NOT NULL,
    budget TEXT,
    contact TEXT NOT NULL,
    extra_json TEXT NOT NULL
);
"""

CREATE_TABLE_LEAD_FILES_SQL = f"""
CREATE TABLE IF NOT EXISTS {LEAD_FILES_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,
    file_type TEXT NOT NULL,
    file_id TEXT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES {LEADS_TABLE}(id) ON DELETE CASCADE
);
"""

CREATE_INDEX_LEAD_FILES_LEAD_ID_SQL = f"""
CREATE INDEX IF NOT EXISTS idx_{LEAD_FILES_TABLE}_lead_id
ON {LEAD_FILES_TABLE}(lead_id);
"""
