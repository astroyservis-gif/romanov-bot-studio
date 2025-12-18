from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def neuro_step1_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Дальше", callback_data="neuro:step1_done")],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="neuro:back"),
                InlineKeyboardButton(text="❌ Отменить", callback_data="lead:cancel"),
            ],
        ]
    )


def neuro_step2_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Продолжить", callback_data="neuro:step2_done")],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="neuro:back"),
                InlineKeyboardButton(text="❌ Отменить", callback_data="lead:cancel"),
            ],
        ]
    )
