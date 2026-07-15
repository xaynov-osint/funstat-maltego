"""User statistics transforms: stats, stats_min, counters, reputation."""

from __future__ import annotations

from .. import entities as E
from ..helpers import FunstatTransform, UIM_INFORM, add_user, apply_props, data_of


class FunstatStats(FunstatTransform):
    """funstat.stats() — full user statistics."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        stats = data_of(fs.stats(request.Value))
        if stats is None:
            response.addUIMessage("Statistics not found.", UIM_INFORM)
            return
        ent = add_user(response, stats, value=request.Value)
        # favorite chat — as a separate property
        fav = getattr(stats, "favorite_chat", None)
        if fav is not None:
            ent.addProperty("funstat.favorite_chat", "Favorite chat", "loose", str(fav.title))


class FunstatStatsMin(FunstatTransform):
    """funstat.stats_min() — brief user statistics."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        stats = data_of(fs.stats_min(request.Value))
        if stats is None:
            response.addUIMessage("Statistics not found.", UIM_INFORM)
            return
        add_user(response, stats, value=request.Value)


class FunstatMessagesCount(FunstatTransform):
    """funstat.messages_count() — total number of the user's messages."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        count = fs.messages_count(request.Value)
        ent = response.addEntity(E.PHRASE, f"Messages: {count}")
        ent.addProperty("funstat.total_msg", "Total messages", "strict", str(count))


class FunstatGroupsCount(FunstatTransform):
    """funstat.groups_count() — number of the user's groups."""

    input_entity = E.TG_USER

    @classmethod
    def run(cls, fs, request, response):
        count = fs.groups_count(request.Value)
        ent = response.addEntity(E.PHRASE, f"Groups: {count}")
        ent.addProperty("funstat.total_groups", "Total groups", "strict", str(count))


class FunstatReputation(FunstatTransform):
    """funstat.rep() — user reputation (votes, average ratings)."""

    input_entity = E.TG_USER

    _SPEC = [
        ("user_id", "funstat.id", "User ID"),
        ("reputation_name", "funstat.reputation_name", "Reputation"),
        ("reputation_code", "funstat.reputation_code", "Reputation code"),
        ("num_votes", "funstat.num_votes", "Votes"),
        ("positive_count", "funstat.positive", "Positive"),
        ("negative_count", "funstat.negative", "Negative"),
        ("anon_votes_count", "funstat.anon_votes", "Anon votes"),
        ("review_count", "funstat.reviews", "Reviews"),
        ("bayesian_average", "funstat.bayesian_avg", "Bayesian avg"),
        ("simple_average", "funstat.simple_avg", "Simple avg"),
        ("first_time", "funstat.first_time", "First vote"),
        ("last_time", "funstat.last_time", "Last vote"),
    ]

    @classmethod
    def run(cls, fs, request, response):
        rep = fs.rep(request.Value)
        if rep is None:
            response.addUIMessage("Reputation not found.", UIM_INFORM)
            return
        ent = response.addEntity(E.TG_USER, request.Value)
        apply_props(ent, rep, cls._SPEC)
