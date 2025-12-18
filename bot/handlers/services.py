from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from bot.constants.portfolio import PORTFOLIO_MEDIA, is_configured
from bot.constants.services import SERVICES
from bot.keyboards.inline import restoration_type_kb
from bot.keyboards.main import main_menu_kb
from bot.keyboards.services import service_card_kb, services_list_kb
from bot.keyboards.portfolio import portfolio_after_album_kb
from bot.keyboards.neuro import neuro_step1_kb
from bot.states.lead_form import LeadForm
from bot.texts.neuro import NEURO_EXAMPLE_PHOTO_FILE_IDS, NEURO_STEP1_TEXT
from bot.texts.services import SERVICE_CARDS_BY_TITLE

router = Router()


def _get_service_title(idx: int) -> str | None:
    if 1 <= idx <= len(SERVICES):
        return SERVICES[idx - 1]
    return None


def _is_restoration_service(title: str) -> bool:
    return "реставрац" in title.lower()


def _is_neuro_service(title: str) -> bool:
    return "нейрофотосесс" in title.lower()


@router.message(F.text == "🧩 Услуги")
async def services_entry(message: Message) -> None:
    await message.answer("Выберите услугу:", reply_markup=services_list_kb(SERVICES))


@router.callback_query(F.data == "services:back_menu")
async def services_back_menu(call: CallbackQuery) -> None:
    await call.message.answer("Главное меню 👇", reply_markup=main_menu_kb())
    await call.answer()


@router.callback_query(F.data == "services:list")
async def services_list(call: CallbackQuery) -> None:
    await call.message.answer("Выберите услугу:", reply_markup=services_list_kb(SERVICES))
    await call.answer()


@router.callback_query(F.data.startswith("services:open:"))
async def services_open(call: CallbackQuery) -> None:
    raw = (call.data or "").split(":", 2)[2]
    try:
        idx = int(raw)
    except ValueError:
        await call.answer("Некорректный выбор")
        return

    title = _get_service_title(idx)
    if not title:
        await call.answer("Некорректный выбор")
        return

    card_text = SERVICE_CARDS_BY_TITLE.get(title, f"{title}\n\nОписание скоро добавим.")
    await call.message.answer(card_text, reply_markup=service_card_kb(idx))
    await call.answer()


@router.callback_query(F.data.startswith("services:apply:"))
async def services_apply(call: CallbackQuery, state: FSMContext) -> None:
    raw = (call.data or "").split(":", 2)[2]
    try:
        idx = int(raw)
    except ValueError:
        await call.answer("Некорректный выбор")
        return

    title = _get_service_title(idx)
    if not title:
        await call.answer("Некорректный выбор")
        return

    await state.clear()
    await state.update_data(service=title, rest_type=None, files=[])

    await call.answer()

    # Стартуем тот же флоу, что и в заявке
    if _is_neuro_service(title):
        await state.set_state(LeadForm.neuro_step1)
        await call.message.answer(NEURO_STEP1_TEXT, reply_markup=neuro_step1_kb())

        # альбом примеров (если настроен)
        if NEURO_EXAMPLE_PHOTO_FILE_IDS:
            media = [InputMediaPhoto(media=fid) for fid in NEURO_EXAMPLE_PHOTO_FILE_IDS[:5]]
            await call.message.answer_media_group(media=media)
        else:
            await call.message.answer("⚠️ Примеры фото пока не настроены (нет file_id).")

        return

    if _is_restoration_service(title):
        await state.set_state(LeadForm.rest_type)
        await call.message.answer("Что реставрируем?", reply_markup=restoration_type_kb())
        return

    await state.set_state(LeadForm.task)
    await call.message.answer("Опишите задачу одним сообщением (что нужно сделать):")
    # дальше обработает lead_flow


@router.callback_query(F.data.startswith("services:portfolio:"))
async def services_portfolio(call: CallbackQuery) -> None:
    raw = (call.data or "").split(":", 2)[2]
    try:
        idx = int(raw)
    except ValueError:
        await call.answer("Некорректный выбор")
        return

    title = _get_service_title(idx)
    if not title:
        await call.answer("Некорректный выбор")
        return

    file_ids = PORTFOLIO_MEDIA[idx - 1]
    if not is_configured(file_ids):
        await call.message.answer(
            f"Примеры для услуги «{title}» пока не настроены.\n"
            "Нужно добавить Telegram file_id изображений в bot/constants/portfolio.py",
            reply_markup=portfolio_after_album_kb(idx),
        )
        await call.answer()
        return

    media = [InputMediaPhoto(media=fid) for fid in file_ids[:5]]
    await call.message.answer_media_group(media=media)
    await call.message.answer("Хотите такой же результат?", reply_markup=portfolio_after_album_kb(idx))
    await call.answer()
