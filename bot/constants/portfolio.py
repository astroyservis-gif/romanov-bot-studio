from __future__ import annotations

from bot.constants.services import SERVICES

# ВАЖНО:
# сюда нужно вставить реальные Telegram file_id изображений.
# На каждую услугу — примерно 5 фото (альбом).
#
# Индексы должны соответствовать SERVICES: 0..len(SERVICES)-1
PORTFOLIO_MEDIA: list[list[str]] = [[] for _ in SERVICES]

# SERVICES[0] — 🧠 Нейрофотосессия
PORTFOLIO_MEDIA[0] = [
    "AgACAgIAAxkBAAIBHmlD8RijmSgacFsTLtBKHnReFpeAAALCDWsbjoQgSkh3styFs-ebAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIBZWlD9tSO6n7bl2wJxYvkQZ8qNYuZAALnDWsbjoQgSrORR_anHQVkAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIBW2lD9jtQ35v_RZJa6d0Dlr_gM5nnAALeDWsbjoQgSolEb75eEaFPAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIBSGlD86YXbBxDPwABdkqW_2GBO8B_tQAC0w1rG46EIEoQda9g21u4tgEAAwIAA3kAAzYE",
    "AgACAgIAAxkBAAIBSmlD8-ucWbjvgAW117PitcuL8kpzAALVDWsbjoQgSqpkkC8kwrqEAQADAgADeQADNgQ",
]


def is_configured(file_ids: list[str]) -> bool:
    # минимальная проверка, чтобы бот не падал, если file_id ещё не заданы
    return bool(file_ids) and all(isinstance(x, str) and x.strip() for x in file_ids)
