from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import aiosqlite

from bot.db.models import (
    CREATE_INDEX_LEAD_FILES_LEAD_ID_SQL,
    CREATE_TABLE_LEAD_FILES_SQL,
    CREATE_TABLE_LEADS_SQL,
)


def _now_iso_utc_seconds() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


async def init_db(db_path: str | Path) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(db_path.as_posix()) as db:
        await db.execute("PRAGMA foreign_keys=ON;")
        await db.execute(CREATE_TABLE_LEADS_SQL)
        await db.execute(CREATE_TABLE_LEAD_FILES_SQL)
        await db.execute(CREATE_INDEX_LEAD_FILES_LEAD_ID_SQL)
        await db.commit()


async def save_lead(
    db_path: str | Path,
    *,
    tg_user_id: int,
    tg_username: str | None,
    tg_full_name: str,
    service: str,
    task: str,
    deadline: str,
    budget: str | None,
    contact: str,
    extra_json: dict[str, Any] | None,
) -> int:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    created_at = _now_iso_utc_seconds()
    extra_json_str = json.dumps(extra_json or {}, ensure_ascii=False)

    async with aiosqlite.connect(db_path.as_posix()) as db:
        await db.execute("PRAGMA foreign_keys=ON;")
        cur = await db.execute(
            """
            INSERT INTO leads (
                created_at, tg_user_id, tg_username, tg_full_name,
                service, task, deadline, budget, contact, extra_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                tg_user_id,
                tg_username,
                tg_full_name,
                service,
                task,
                deadline,
                budget,
                contact,
                extra_json_str,
            ),
        )
        await db.commit()
        lead_id = int(cur.lastrowid)
        return lead_id


async def save_files(
    db_path: str | Path,
    *,
    lead_id: int,
    files: Iterable[dict[str, str]],
) -> None:
    """
    files: iterable of {"file_type": "...", "file_id": "..."}
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[tuple[int, str, str]] = []
    for f in files:
        file_type = (f.get("file_type") or "").strip()
        file_id = (f.get("file_id") or "").strip()
        if not file_type or not file_id:
            continue
        rows.append((lead_id, file_type, file_id))

    if not rows:
        return

    async with aiosqlite.connect(db_path.as_posix()) as db:
        await db.execute("PRAGMA foreign_keys=ON;")
        await db.executemany(
            """
            INSERT INTO lead_files (lead_id, file_type, file_id)
            VALUES (?, ?, ?)
            """,
            rows,
        )
        await db.commit()
