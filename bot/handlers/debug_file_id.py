from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.photo)
async def debug_photo_file_id(message: Message) -> None:
    file_id = message.photo[-1].file_id
    await message.answer(f"file_id:\n<code>{file_id}</code>")
