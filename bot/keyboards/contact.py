from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def contact_choice_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Использовать мой @username")],
            [KeyboardButton(text="📞 Указать телефон"), KeyboardButton(text="✍️ Ввести другой контакт")],
            [KeyboardButton(text="⏭ Пропустить")],
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Отменить")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите вариант контакта…",
    )


def contact_input_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Отменить")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Введите контакт…",
    )
