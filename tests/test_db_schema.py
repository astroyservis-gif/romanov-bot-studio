from __future__ import annotations

import aiosqlite
import pytest

from bot.db.models import LEADS_COLUMNS, LEAD_FILES_COLUMNS


@pytest.mark.asyncio
async def test_db_schema_tables_and_columns(inited_db):
    db_path = inited_db

    async with aiosqlite.connect(str(db_path)) as db:
        # tables exist
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('leads','lead_files')"
        ) as cur:
            rows = await cur.fetchall()
        names = {r[0] for r in rows}
        assert "leads" in names
        assert "lead_files" in names

        # leads columns
        async with db.execute("PRAGMA table_info(leads)") as cur:
            leads_info = await cur.fetchall()
        leads_cols = [r[1] for r in leads_info]
        assert leads_cols == list(LEADS_COLUMNS)

        # lead_files columns
        async with db.execute("PRAGMA table_info(lead_files)") as cur:
            files_info = await cur.fetchall()
        files_cols = [r[1] for r in files_info]
        assert files_cols == list(LEAD_FILES_COLUMNS)
