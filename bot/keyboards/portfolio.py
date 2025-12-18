from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def portfolio_services_kb(services: list[str]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for idx, title in enumerate(services, start=1):
        rows.append([InlineKeyboardButton(text=title, callback_data=f"pf:svc:{idx}")])
    rows.append([InlineKeyboardButton(text="Отменить", callback_data="pf:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def portfolio_after_album_kb(service_idx: int) -> InlineKeyboardMarkup:
    # service_idx: 1..N
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оставить заявку", callback_data=f"lead:svc:{service_idx}")],
            [InlineKeyboardButton(text="⬅️ Назад к списку услуг", callback_data="pf:back")],
        ]
    )
