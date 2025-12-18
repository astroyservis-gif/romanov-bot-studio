from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    choosing_service = State()

    # общий поток
    task = State()
    deadline = State()
    deadline_custom = State()

    # контакт (улучшенный UX)
    contact_choice = State()
    contact_phone = State()
    contact_other = State()

    confirm = State()

    # сценарий "Реставрация фото/видео" + файлы
    rest_type = State()
    files = State()

    # сценарий "Нейрофотосессия" (инструкции -> пожелания)
    neuro_step1 = State()
    neuro_step2 = State()
    neuro_wishes = State()
