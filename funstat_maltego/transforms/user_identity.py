"""Трансформы идентификации пользователя: резолв, базовая инфа, имена, юзернеймы."""

from __future__ import annotations

from .. import entities as E
from ..helpers import (
    FunstatTransform,
    UIM_INFORM,
    add_group,
    add_user,
    data_of,
    parse_ids,
)


class FunstatResolveUsername(FunstatTransform):
    """funstat.resolve_username() — @username → пользователи Telegram."""

    input_entity = E.TG_USERNAME

    @classmethod
    def run(cls, fs, request, response):
        users = data_of(fs.resolve_username(request.Value)) or []
        if not users:
            response.addUIMessage("Пользователь не найден.", UIM_INFORM)
            return
        for user in users:
            add_user(response, user)


class FunstatBasicInfo(FunstatTransform):
    """funstat.basic_info_by_id() — базовая инфа по одному или нескольким id."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        ids = parse_ids(request.Value)
        payload = ids if len(ids) > 1 else request.Value
        users = data_of(fs.basic_info_by_id(payload)) or []
        if not users:
            response.addUIMessage("Данные не найдены.", UIM_INFORM)
            return
        for user in users:
            add_user(response, user)


class FunstatGetNames(FunstatTransform):
    """funstat.get_names() — история отображаемых имён пользователя."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        names = data_of(fs.get_names(request.Value)) or []
        if not names:
            response.addUIMessage("Имена не найдены.", UIM_INFORM)
            return
        for item in names:
            ent = response.addEntity(E.PERSON_NAME, item.name)
            ent.addProperty("funstat.name", "Name", "loose", item.name)
            ent.addProperty("funstat.date_time", "Seen at", "loose", str(item.date_time))
            ent.addDisplayInformation(f"{item.name}<br/>{item.date_time}", "Name history")


class FunstatGetUsernames(FunstatTransform):
    """funstat.get_usernames() — история @username пользователя."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        usernames = data_of(fs.get_usernames(request.Value)) or []
        if not usernames:
            response.addUIMessage("Юзернеймы не найдены.", UIM_INFORM)
            return
        for item in usernames:
            ent = response.addEntity(E.TG_USERNAME, item.name)
            ent.addProperty("funstat.username", "Username", "loose", item.name)
            ent.addProperty("funstat.date_time", "Seen at", "loose", str(item.date_time))
            ent.addDisplayInformation(f"{item.name}<br/>{item.date_time}", "Username history")


class FunstatUsernameUsage(FunstatTransform):
    """funstat.username_usage() — кто/что использует данный @username сейчас и в прошлом."""

    input_entity = E.TG_USERNAME

    @classmethod
    def run(cls, fs, request, response):
        usage = data_of(fs.username_usage(request.Value))
        if usage is None:
            response.addUIMessage("Использование юзернейма не найдено.", UIM_INFORM)
            return

        for user in (usage.actual_users or []):
            add_user(response, user).setLinkLabel("actual user")
        for user in (usage.usage_by_users_in_the_past or []):
            add_user(response, user).setLinkLabel("past user")
        for group in (usage.actual_groups_or_channels or []):
            add_group(response, group).setLinkLabel("actual group/channel")
        for group in (usage.mention_by_channel_or_group_desc or []):
            add_group(response, group).setLinkLabel("mentioned in description")
