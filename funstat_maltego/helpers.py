"""Базовый класс трансформы, обработка ошибок и билдеры сущностей."""

from __future__ import annotations

from typing import Iterable, Sequence

from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from .client import FunstatDependencyError, FunstatTokenError, open_client
from . import entities as E

# Типы UI-сообщений Maltego.
UIM_PARTIAL = "PartialError"
UIM_FATAL = "FatalError"
UIM_INFORM = "Inform"


# --------------------------------------------------------------------------- #
# Базовый класс
# --------------------------------------------------------------------------- #
class FunstatTransform(DiscoverableTransform):
    """Общий каркас: открывает клиента, ловит ошибки, делегирует в ``run``.

    Наследники обязаны реализовать classmethod ``run(cls, fs, request, response)``,
    где ``fs`` — уже открытый ``FunstatClient``.
    """

    # Тип входной сущности — только для документации/справки.
    input_entity = E.PHRASE

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform) -> None:
        # Если запуск с Telegram-сущности (maltego.affiliation.Telegram),
        # предпочитаем её UID как точный идентификатор для API.
        try:
            uid = request.getProperty("affiliation.uid")
        except Exception:  # noqa: BLE001
            uid = None
        if uid and str(uid).strip():
            request.Value = str(uid).strip()

        if not request.Value or not request.Value.strip():
            response.addUIMessage("Пустое входное значение.", UIM_PARTIAL)
            return

        try:
            client = open_client()
        except (FunstatTokenError, FunstatDependencyError) as exc:
            response.addUIMessage(str(exc), UIM_PARTIAL)
            return

        try:
            with client as fs:
                cls.run(fs, request, response)
        except Exception as exc:  # noqa: BLE001 — трансформа не должна падать
            response.addUIMessage(f"Ошибка funstat-api: {exc}", UIM_PARTIAL)

    @classmethod
    def run(cls, fs, request: MaltegoMsg, response: MaltegoTransform) -> None:
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# Утилиты
# --------------------------------------------------------------------------- #
def data_of(resp):
    """Достать ``.data`` из ответа (или сам объект, если обёртки нет)."""
    if resp is None:
        return None
    return getattr(resp, "data", resp)


def parse_ids(raw: str) -> list[str]:
    """Разобрать строку с несколькими id (через запятую/пробел/перевод строки)."""
    parts = raw.replace(",", " ").replace(";", " ").split()
    return [p.strip() for p in parts if p.strip()]


def slider_limit(request: MaltegoMsg, default: int = 20) -> int:
    """Лимит результатов из ползунка Maltego (если задан)."""
    try:
        val = int(getattr(request, "Slider", 0) or 0)
        return val if val > 0 else default
    except (TypeError, ValueError):
        return default


def _str(value) -> str:
    return "" if value is None else str(value)


def apply_props(entity, model, spec: Sequence[tuple[str, str, str]]):
    """Навесить свойства из модели на сущность и собрать Detail View.

    ``spec`` — последовательность кортежей ``(attr, field_id, display_name)``.
    Отсутствующие/``None`` поля пропускаются.
    """
    lines: list[str] = []
    for attr, field_id, display in spec:
        value = getattr(model, attr, None)
        if value is None or value == "":
            continue
        entity.addProperty(field_id, display, "loose", _str(value))
        lines.append(f"{display}: {value}")
    if lines:
        entity.addDisplayInformation("<br/>".join(lines), "Funstat")
    return entity


# --------------------------------------------------------------------------- #
# Билдеры сущностей из моделей funstat
# --------------------------------------------------------------------------- #
_USER_SPEC = [
    ("id", "funstat.id", "ID"),
    ("username", "funstat.username", "Username"),
    ("first_name", "funstat.first_name", "First name"),
    ("last_name", "funstat.last_name", "Last name"),
    ("is_bot", "funstat.is_bot", "Is bot"),
    ("is_active", "funstat.is_active", "Is active"),
    ("has_premium", "funstat.has_premium", "Premium"),
    ("has_prem", "funstat.has_premium", "Premium"),
    ("is_user_active", "funstat.is_active", "Is active"),
    ("name", "funstat.name", "Name"),
    # статистика (UserStatsMin / UserStats)
    ("total_msg_count", "funstat.total_msg", "Total messages"),
    ("msg_in_groups_count", "funstat.msg_in_groups", "Messages in groups"),
    ("adm_in_groups", "funstat.adm_in_groups", "Admin in groups"),
    ("total_groups", "funstat.total_groups", "Total groups"),
    ("usernames_count", "funstat.usernames_count", "Usernames count"),
    ("names_count", "funstat.names_count", "Names count"),
    ("first_msg_date", "funstat.first_msg_date", "First message"),
    ("last_msg_date", "funstat.last_msg_date", "Last message"),
    ("lang_code", "funstat.lang_code", "Language"),
    ("unique_percent", "funstat.unique_percent", "Unique %"),
    ("reply_percent", "funstat.reply_percent", "Reply %"),
    ("media_percent", "funstat.media_percent", "Media %"),
    ("link_percent", "funstat.link_percent", "Link %"),
    ("voice_count", "funstat.voice_count", "Voice count"),
    ("circle_count", "funstat.circle_count", "Circle count"),
    ("stars_val", "funstat.stars", "Stars"),
    ("gift_count", "funstat.gift_count", "Gifts"),
    ("about", "funstat.about", "About"),
    ("common_groups", "funstat.common_groups", "Common groups"),
    ("today_msg", "funstat.today_msg", "Messages today"),
    ("is_admin", "funstat.is_admin", "Is admin"),
    ("dc_id", "funstat.dc_id", "DC id"),
]


def _user_value(model, fallback: str = "") -> str:
    username = getattr(model, "username", None)
    uid = getattr(model, "id", None) or getattr(model, "user_id", None)
    return username or (str(uid) if uid is not None else fallback)


def add_user(response: MaltegoTransform, model, value: str | None = None):
    entity = response.addEntity(E.TG_USER, value or _user_value(model))
    apply_props(entity, model, _USER_SPEC)
    # Нативные поля Telegram-сущности: UID для точного резолва при повторных
    # запусках трансформ по этому пользователю.
    uid = getattr(model, "id", None) or getattr(model, "user_id", None)
    if uid is not None:
        entity.addProperty("affiliation.uid", "Telegram UID", "strict", str(uid))
    return entity


_GROUP_SPEC = [
    ("id", "funstat.group_id", "Group ID"),
    ("title", "funstat.title", "Title"),
    ("username", "funstat.group_username", "Username"),
    ("link", "funstat.link", "Link"),
    ("is_private", "funstat.is_private", "Private"),
    ("is_channel", "funstat.is_channel", "Channel"),
    ("members_count", "funstat.members_count", "Members"),
    ("about", "funstat.group_about", "About"),
    ("is_scam", "funstat.is_scam", "Scam"),
    ("is_fake", "funstat.is_fake", "Fake"),
    ("has_photo", "funstat.has_photo", "Has photo"),
    # UsrChatInfo-специфика
    ("messages_count", "funstat.chat_msg_count", "Messages in chat"),
    ("last_message", "funstat.last_message", "Last message"),
    ("is_admin", "funstat.is_admin", "Is admin"),
    ("is_left", "funstat.is_left", "Left"),
]


def add_group(response: MaltegoTransform, model, value: str | None = None):
    title = getattr(model, "title", None)
    gid = getattr(model, "id", None)
    entity = response.addEntity(E.TG_GROUP, value or title or _str(gid))
    apply_props(entity, model, _GROUP_SPEC)
    return entity
