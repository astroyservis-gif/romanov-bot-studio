from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def services_list_kb(services: list[str]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for idx, title in enumerate(services, start=1):
        rows.append([InlineKeyboardButton(text=title, callback_data=f"services:open:{idx}")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="services:back_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def service_card_kb(service_idx: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оставить заявку", callback_data=f"services:apply:{service_idx}")],
            [InlineKeyboardButton(text="🖼 Примеры работ", callback_data=f"services:portfolio:{service_idx}")],
            [InlineKeyboardButton(text="⬅️ К услугам", callback_data="services:list")],
        ]
    )
