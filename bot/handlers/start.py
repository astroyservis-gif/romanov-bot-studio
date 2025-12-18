from __future__ import annotations

from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import Router

from bot.keyboards.main import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "Привет! Это <b>Romanov Bot Studio</b>.\n"
        "Выберите действие ниже 👇"
    )
    await message.answer(text, reply_markup=main_menu_kb())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "<b>Помощь</b>\n"
        "Нажмите «✅ Оставить заявку», чтобы оформить запрос.\n"
        "Можно открыть «🧩 Услуги» или «🖼 Примеры работ»."
    )
    await message.answer(text, reply_markup=main_menu_kb())
