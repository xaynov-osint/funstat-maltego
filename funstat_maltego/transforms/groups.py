"""Трансформы по группам/каналам: инфо о группе, участники, общие группы для набора id."""

from __future__ import annotations

from .. import entities as E
from ..helpers import (
    FunstatTransform,
    UIM_INFORM,
    add_group,
    add_user,
    apply_props,
    data_of,
    parse_ids,
)


class FunstatGroupInfo(FunstatTransform):
    """funstat.get_group_info() — карточка группы/канала + дневная статистика."""

    input_entity = E.TG_GROUP

    _STAT_SPEC = [
        ("rank", "funstat.rank", "Rank"),
        ("active_users_count", "funstat.active_users", "Active users"),
        ("messages_count", "funstat.today_messages", "Messages today"),
        ("text_msg_count", "funstat.text_msg", "Text messages"),
        ("media_msg_count", "funstat.media_msg", "Media messages"),
        ("voice_count", "funstat.voice", "Voice"),
        ("circle_count", "funstat.circle", "Circle"),
        ("non_cyrillic_rate", "funstat.non_cyrillic", "Non-cyrillic %"),
        ("avg_unique_percent", "funstat.avg_unique", "Avg unique %"),
        ("avg_media_percent", "funstat.avg_media", "Avg media %"),
        ("avg_link_percent", "funstat.avg_link", "Avg link %"),
    ]

    @classmethod
    def run(cls, fs, request, response):
        res = fs.get_group_info(request.Value)
        if res is None or getattr(res, "info", None) is None:
            response.addUIMessage("Группа не найдена.", UIM_INFORM)
            return
        ent = add_group(response, res.info)
        stat = getattr(res, "today_group_stat", None)
        if stat is not None:
            apply_props(ent, stat, cls._STAT_SPEC)


class FunstatGroupMembers(FunstatTransform):
    """funstat.get_group_members() — участники группы."""

    input_entity = E.TG_GROUP

    @classmethod
    def run(cls, fs, request, response):
        members = data_of(fs.get_group_members(request.Value)) or []
        if not members:
            response.addUIMessage("Участники не найдены.", UIM_INFORM)
            return
        for member in members:
            add_user(response, member)


class FunstatCommonGroupsForUsers(FunstatTransform):
    """funstat.common_groups_for_users() — общие группы для набора пользователей.

    Вход: сущность со значением из нескольких id/username (через запятую/пробел).
    """

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        ids = parse_ids(request.Value)
        if len(ids) < 2:
            response.addUIMessage(
                "Нужно 2+ id/username (через запятую или пробел) во входном значении.",
                UIM_INFORM,
            )
            return
        groups = data_of(fs.common_groups_for_users(ids)) or []
        if not groups:
            response.addUIMessage("Общих групп не найдено.", UIM_INFORM)
            return
        for group in groups:
            add_group(response, group)
