from __future__ import annotations

from pathlib import Path

import pytest_asyncio

from bot.db.repository import init_db


@pytest_asyncio.fixture
async def inited_db(tmp_path: Path) -> Path:
    """
    Создаёт временную БД в tmp_path и инициализирует схему.
    Возвращает путь к файлу БД.
    """
    db_path = tmp_path / "test.db"
    await init_db(db_path)
    return db_path
