from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def back_cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Отменить")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Введите ответ…",
    )
