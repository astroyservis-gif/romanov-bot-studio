from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Оставить заявку")],
            [KeyboardButton(text="🧩 Услуги"), KeyboardButton(text="🧾 Как мы работаем")],
            [KeyboardButton(text="🖼 Примеры работ"), KeyboardButton(text="☎️ Контакты")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие…",
    )
