from __future__ import annotations

from typing import Any


_DEADLINE_MAP: dict[str, str] = {
    "urgent": "Срочно (1–2 дня)",
    "week": "В течение недели",
    "not_urgent": "Не срочно",
}


def map_deadline(deadline_key: str, custom_text: str | None = None) -> str:
    key = (deadline_key or "").strip()
    if key.startswith("deadline:"):
        key = key.split(":", 1)[1].strip()

    if key == "custom":
        text = (custom_text or "").strip()
        return text if text else "Свой вариант"

    return _DEADLINE_MAP.get(key, key if key else "Не указано")


def prepare_lead_data(
    *,
    tg_user_id: int,
    tg_username: str | None,
    tg_full_name: str,
    service: str,
    task: str,
    deadline_key: str,
    deadline_custom_text: str | None = None,
    budget: str | None = None,
    contact: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "tg_user_id": int(tg_user_id),
        "tg_username": (tg_username or "").strip() or None,
        "tg_full_name": (tg_full_name or "").strip(),
        "service": (service or "").strip(),
        "task": (task or "").strip(),
        "deadline": map_deadline(deadline_key, deadline_custom_text),
        "budget": (budget or "").strip() or None,
        "contact": (contact or "").strip(),
        "extra_json": extra or {},
    }


def format_admin_message(
    lead: dict[str, Any],
    files: list[dict[str, str]] | None = None,
) -> str:
    full_name = (lead.get("tg_full_name") or "").strip() or "Без имени"
    username = lead.get("tg_username")
    username_part = f" (@{username})" if username else ""

    service = (lead.get("service") or "").strip()
    task = (lead.get("task") or "").strip()
    deadline = (lead.get("deadline") or "").strip()
    budget = (lead.get("budget") or "").strip()
    contact = (lead.get("contact") or "").strip()

    lines: list[str] = []
    lines.append("🆕 Новая заявка")
    lines.append(f"От: {full_name}{username_part}")
    lines.append(f"Услуга: {service}")
    lines.append(f"Задача: {task}")
    lines.append(f"Срок: {deadline}")
    if budget:
        lines.append(f"Бюджет: {budget}")
    lines.append(f"Контакт: {contact}")

    file_lines: list[str] = []
    for f in (files or []):
        ft = (f.get("file_type") or "").strip()
        fid = (f.get("file_id") or "").strip()
        if ft and fid:
            file_lines.append(f"- {ft}: {fid}")

    if file_lines:
        lines.append("Файлы:")
        lines.extend(file_lines)

    return "\n".join(lines)
