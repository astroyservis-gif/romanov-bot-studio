from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import ADMIN_TG_ID, DB_PATH
from bot.db.repository import save_lead
from bot.keyboards.form import back_cancel_kb
from bot.keyboards.inline import confirm_kb, deadline_kb, services_kb
from bot.keyboards.main import main_menu_kb
from bot.services.leads import format_admin_message, prepare_lead_data
from bot.states.lead_form import LeadForm
from bot.utils.validators import is_non_empty_text, validate_contact

router = Router()

SERVICES: list[str] = [
    "🧠 Нейрофотосессия",
    "🧹 Реставрация фото",
    "🎬 Видеопоздравление",
    "📣 Контент для соцсетей/рекла",
    "🖼 Ролики и истории из фотографий",
]

_DEADLINE_LABELS: dict[str, str] = {
    "urgent": "Срочно",
    "week": "В течение недели",
    "not_urgent": "Не срочно",
}


async def _cancel_flow(target: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = "Ок, отменил. Возвращаю в меню 👇"
    if isinstance(target, CallbackQuery):
        await target.message.answer(text, reply_markup=main_menu_kb())
        await target.answer()
    else:
        await target.answer(text, reply_markup=main_menu_kb())


def _summary_text(data: dict) -> str:
    service = data.get("service") or "—"
    task = data.get("task") or "—"
    deadline = data.get("deadline") or "—"
    contact = data.get("contact") or "—"

    return (
        "<b>Проверь заявку</b>\n\n"
        f"<b>Услуга:</b> {service}\n"
        f"<b>Задача:</b> {task}\n"
        f"<b>Срок:</b> {deadline}\n"
        f"<b>Контакт:</b> {contact}\n\n"
        "Если всё верно — жми «Отправить»."
    )


async def _ask_task(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    service = data.get("service") or ""
    prefix = f"Ок. Услуга: <b>{service}</b>\n\n" if service else ""
    await state.set_state(LeadForm.task)
    await message.answer(
        prefix + "Опишите задачу одним сообщением (что нужно сделать):",
        reply_markup=back_cancel_kb(),
    )


async def _ask_deadline(message: Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.deadline)
    await message.answer("Выберите срочность:", reply_markup=deadline_kb())


async def _ask_contact(message: Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.contact)
    await message.answer(
        "Оставьте контакт для связи (телефон / @username / ссылка):",
        reply_markup=back_cancel_kb(),
    )


async def _show_confirm(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(LeadForm.confirm)
    await message.answer(_summary_text(data), reply_markup=confirm_kb())


@router.message(F.text == "✅ Оставить заявку")
async def start_lead_flow(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.choosing_service)
    await message.answer(
        "Выберите услугу:",
        reply_markup=services_kb(SERVICES),
    )


@router.message(F.text == "❌ Отменить")
async def cancel_from_reply(message: Message, state: FSMContext) -> None:
    current = await state.get_state()
    if current is None:
        await message.answer("Вы в меню.", reply_markup=main_menu_kb())
        return
    await _cancel_flow(message, state)


@router.callback_query(F.data == "lead:cancel")
async def lead_cancel(call: CallbackQuery, state: FSMContext) -> None:
    await _cancel_flow(call, state)


@router.callback_query(LeadForm.choosing_service, F.data.startswith("svc:"))
async def choose_service(call: CallbackQuery, state: FSMContext) -> None:
    raw = (call.data or "").split(":", 1)[1]
    try:
        idx = int(raw)
    except ValueError:
        await call.answer("Некорректный выбор")
        return

    if not (1 <= idx <= len(SERVICES)):
        await call.answer("Некорректный выбор")
        return

    service = SERVICES[idx - 1]
    await state.update_data(service=service)

    await call.answer()
    await _ask_task(call.message, state)


@router.message(F.text == "⬅️ Назад")
async def back_from_reply(message: Message, state: FSMContext) -> None:
    current = await state.get_state()

    if current == LeadForm.task.state:
        await state.set_state(LeadForm.choosing_service)
        await message.answer("Выберите услугу:", reply_markup=services_kb(SERVICES))
        return

    if current == LeadForm.deadline_custom.state:
        await _ask_deadline(message, state)
        return

    if current == LeadForm.contact.state:
        await _ask_deadline(message, state)
        return

    await message.answer("Вы в меню.", reply_markup=main_menu_kb())


@router.callback_query(F.data == "lead:back")
async def back_from_inline(call: CallbackQuery, state: FSMContext) -> None:
    current = await state.get_state()

    if current == LeadForm.deadline.state:
        await call.answer()
        await _ask_task(call.message, state)
        return

    if current == LeadForm.confirm.state:
        await call.answer()
        await _ask_contact(call.message, state)
        return

    await call.answer()


@router.message(LeadForm.task)
async def input_task(message: Message, state: FSMContext) -> None:
    task = (message.text or "").strip()
    if not is_non_empty_text(task):
        await message.answer("Напишите задачу текстом (не пусто).", reply_markup=back_cancel_kb())
        return

    await state.update_data(task=task)
    await _ask_deadline(message, state)


@router.callback_query(LeadForm.deadline, F.data.startswith("dl:"))
async def choose_deadline(call: CallbackQuery, state: FSMContext) -> None:
    key = (call.data or "").split(":", 1)[1].strip()

    if key == "custom":
        await state.set_state(LeadForm.deadline_custom)
        await call.message.answer(
            "Напишите ваш вариант срока (например: «к пятнице», «до 10 января»):",
            reply_markup=back_cancel_kb(),
        )
        await call.answer()
        return

    if key not in _DEADLINE_LABELS:
        await call.answer("Некорректный выбор")
        return

    await state.update_data(deadline=_DEADLINE_LABELS[key])

    await call.answer()
    await _ask_contact(call.message, state)


@router.message(LeadForm.deadline_custom)
async def input_deadline_custom(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not is_non_empty_text(text):
        await message.answer("Напишите срок текстом (не пусто).", reply_markup=back_cancel_kb())
        return

    await state.update_data(deadline=text)
    await _ask_contact(message, state)


@router.message(LeadForm.contact)
async def input_contact(message: Message, state: FSMContext) -> None:
    contact = (message.text or "").strip()
    if not validate_contact(contact):
        await message.answer("Контакт слишком короткий. Напишите минимум 3 символа.", reply_markup=back_cancel_kb())
        return

    await state.update_data(contact=contact)
    await _show_confirm(message, state)


@router.callback_query(LeadForm.confirm, F.data == "lead:edit")
async def lead_edit(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.choosing_service)
    await call.message.answer("Ок, давайте заново. Выберите услугу:", reply_markup=services_kb(SERVICES))
    await call.answer()


@router.callback_query(LeadForm.confirm, F.data == "lead:send")
async def lead_send(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    service = (data.get("service") or "").strip()
    task = (data.get("task") or "").strip()
    deadline = (data.get("deadline") or "").strip()
    contact = (data.get("contact") or "").strip()

    if not (service and task and deadline and contact):
        await call.answer("Данные заявки неполные. Начните заново.", show_alert=True)
        await _cancel_flow(call, state)
        return

    user = call.from_user
    lead = prepare_lead_data(
        tg_user_id=user.id,
        tg_username=user.username,
        tg_full_name=(user.full_name or "").strip() or "Пользователь",
        service=service,
        task=task,
        deadline_key="deadline:custom",
        deadline_custom_text=deadline,
        budget=None,
        contact=contact,
        extra={},
    )
    lead["deadline"] = deadline

    lead_id = await save_lead(
        DB_PATH,
        tg_user_id=lead["tg_user_id"],
        tg_username=lead["tg_username"],
        tg_full_name=lead["tg_full_name"],
        service=lead["service"],
        task=lead["task"],
        deadline=lead["deadline"],
        budget=lead["budget"],
        contact=lead["contact"],
        extra_json=lead["extra_json"],
    )

    admin_text = format_admin_message(lead, files=None)
    await call.bot.send_message(ADMIN_TG_ID, admin_text)

    await state.clear()
    await call.message.answer(
        f"✅ Заявка отправлена! Номер: <b>{lead_id}</b>\n"
        "Мы свяжемся с вами в ближайшее время.",
        reply_markup=main_menu_kb(),
    )
    await call.answer()
