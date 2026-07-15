"""Activity transforms: messages, chats, stickers, gifts, common groups, text search."""

from __future__ import annotations

from .. import entities as E
from ..helpers import (
    FunstatTransform,
    UIM_INFORM,
    add_group,
    add_user,
    data_of,
    slider_limit,
)


class FunstatGetMessages(FunstatTransform):
    """funstat.get_messages() — the user's messages (+ groups where they were posted)."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        limit = slider_limit(request, 20)
        msgs = data_of(fs.get_messages(request.Value, limit=limit)) or []
        if not msgs:
            response.addUIMessage("No messages found.", UIM_INFORM)
            return
        for msg in msgs:
            text = msg.text or f"[media #{msg.message_id}]"
            ent = response.addEntity(E.TG_MESSAGE, text[:120])
            ent.addProperty("funstat.message_id", "Message ID", "loose", str(msg.message_id))
            ent.addProperty("funstat.date", "Date", "loose", str(msg.date))
            if msg.media_name:
                ent.addProperty("funstat.media", "Media", "loose", str(msg.media_name))
            if msg.group is not None:
                ent.addProperty("funstat.group", "Group", "loose", str(msg.group.title))
                add_group(response, msg.group)
            ent.addDisplayInformation(
                f"[{msg.date}] {text}", "Message"
            )


class FunstatGetChats(FunstatTransform):
    """funstat.get_chats() — chats/groups the user is a member of."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        chats = data_of(fs.get_chats(request.Value)) or []
        if not chats:
            response.addUIMessage("No chats found.", UIM_INFORM)
            return
        for item in chats:
            # UsrChatInfo: nested .chat + top-level metrics
            chat = getattr(item, "chat", item)
            ent = add_group(response, chat)
            for attr, fid, disp in [
                ("messages_count", "funstat.chat_msg_count", "Messages"),
                ("last_message", "funstat.last_message", "Last message"),
                ("is_admin", "funstat.is_admin", "Is admin"),
                ("is_left", "funstat.is_left", "Left"),
            ]:
                val = getattr(item, attr, None)
                if val is not None and val != "":
                    ent.addProperty(fid, disp, "loose", str(val))


class FunstatCommonGroups(FunstatTransform):
    """funstat.common_groups() — users with whom there are common groups."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        users = data_of(fs.common_groups(request.Value)) or []
        if not users:
            response.addUIMessage("No common groups found.", UIM_INFORM)
            return
        for user in users:
            ent = add_user(response, user)
            cg = getattr(user, "common_groups", None)
            if cg is not None:
                ent.setLinkLabel(f"{cg} common")


class FunstatGetStickers(FunstatTransform):
    """funstat.get_stickers() — sticker packs used by the user."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        stickers = data_of(fs.get_stickers(request.Value)) or []
        if not stickers:
            response.addUIMessage("No stickers found.", UIM_INFORM)
            return
        for st in stickers:
            value = st.short_name or st.title or str(st.sticker_set_id)
            ent = response.addEntity(E.TG_STICKER, value)
            for attr, fid, disp in [
                ("sticker_set_id", "funstat.sticker_set_id", "Set ID"),
                ("title", "funstat.title", "Title"),
                ("short_name", "funstat.short_name", "Short name"),
                ("stickers_count", "funstat.stickers_count", "Count"),
                ("last_seen", "funstat.last_seen", "Last seen"),
                ("min_seen", "funstat.min_seen", "First seen"),
            ]:
                val = getattr(st, attr, None)
                if val is not None and val != "":
                    ent.addProperty(fid, disp, "loose", str(val))


class FunstatGetGifts(FunstatTransform):
    """funstat.get_gifts() — the user's gifts (senders/recipients)."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        limit = slider_limit(request, 20)
        gifts = data_of(fs.get_gifts(request.Value, limit=limit)) or []
        if not gifts:
            response.addUIMessage("No gifts found.", UIM_INFORM)
            return
        for g in gifts:
            sender = response.addEntity(
                E.TG_USER, g.from_main_username or str(g.from_user_id)
            )
            sender.addProperty("funstat.id", "ID", "loose", str(g.from_user_id))
            sender.addProperty("funstat.first_name", "First name", "loose", str(g.from_first_name or ""))
            sender.setLinkLabel(f"gift → {g.to_user_id}")

            recipient = response.addEntity(
                E.TG_USER, g.to_main_username or str(g.to_user_id)
            )
            recipient.addProperty("funstat.id", "ID", "loose", str(g.to_user_id))
            recipient.addProperty("funstat.first_name", "First name", "loose", str(g.to_first_name or ""))
            if g.last_gift_date:
                recipient.addProperty("funstat.last_gift_date", "Last gift", "loose", str(g.last_gift_date))
            recipient.setLinkLabel("gift recipient")


class FunstatSearchText(FunstatTransform):
    """funstat.search_text() — who wrote the given text and where. Input: maltego.Phrase."""

    input_entity = E.PHRASE

    @classmethod
    def run(cls, fs, request, response):
        page_size = slider_limit(request, 20)
        paged = data_of(fs.search_text(request.Value, page=1, page_size=page_size))
        rows = getattr(paged, "data", None) or []
        if not rows:
            response.addUIMessage("No matches found.", UIM_INFORM)
            return
        for row in rows:
            text = row.text or f"[message #{row.message_id}]"
            ent = response.addEntity(E.TG_MESSAGE, text[:120])
            ent.addProperty("funstat.message_id", "Message ID", "loose", str(row.message_id))
            ent.addProperty("funstat.date", "Date", "loose", str(row.date))
            ent.addProperty("funstat.user_id", "Author ID", "loose", str(row.user_id))
            if row.username:
                ent.addProperty("funstat.username", "Author", "loose", str(row.username))
            if row.group is not None:
                ent.addProperty("funstat.group", "Group", "loose", str(row.group.title))
                add_group(response, row.group)
            # author as a separate entity
            author = response.addEntity(E.TG_USER, row.username or str(row.user_id))
            author.addProperty("funstat.id", "ID", "loose", str(row.user_id))
            if row.name:
                author.addProperty("funstat.name", "Name", "loose", str(row.name))
