from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from bot.constants.portfolio import PORTFOLIO_MEDIA, is_configured
from bot.constants.services import SERVICES
from bot.keyboards.main import main_menu_kb
from bot.keyboards.portfolio import portfolio_after_album_kb, portfolio_services_kb

router = Router()


@router.message(F.text == "🖼 Примеры работ")
async def portfolio_entry(message: Message) -> None:
    await message.answer(
        "Выберите услугу, чтобы посмотреть примеры:",
        reply_markup=portfolio_services_kb(SERVICES),
    )


@router.callback_query(F.data == "pf:cancel")
async def portfolio_cancel(call: CallbackQuery) -> None:
    await call.message.answer("Ок. Возвращаю в меню 👇", reply_markup=main_menu_kb())
    await call.answer()


@router.callback_query(F.data == "pf:back")
async def portfolio_back(call: CallbackQuery) -> None:
    await call.message.answer(
        "Выберите услугу, чтобы посмотреть примеры:",
        reply_markup=portfolio_services_kb(SERVICES),
    )
    await call.answer()


@router.callback_query(F.data.startswith("pf:svc:"))
async def portfolio_choose_service(call: CallbackQuery) -> None:
    raw = (call.data or "").split(":", 2)[2]
    try:
        idx = int(raw)
    except ValueError:
        await call.answer("Некорректный выбор")
        return

    if not (1 <= idx <= len(SERVICES)):
        await call.answer("Некорректный выбор")
        return

    service_title = SERVICES[idx - 1]
    file_ids = PORTFOLIO_MEDIA[idx - 1]

    # Если file_id ещё не настроены — не падаем, а говорим как исправить
    if not is_configured(file_ids):
        await call.message.answer(
            f"Примеры для услуги «{service_title}» пока не настроены.\n"
            "Нужно добавить Telegram file_id изображений в bot/constants/portfolio.py",
            reply_markup=portfolio_after_album_kb(idx),
        )
        await call.answer()
        return

    media = [InputMediaPhoto(media=fid) for fid in file_ids[:5]]
    await call.message.answer_media_group(media=media)

    await call.message.answer(
        "Хотите такой же результат?",
        reply_markup=portfolio_after_album_kb(idx),
    )
    await call.answer()
