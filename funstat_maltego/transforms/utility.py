"""Служебные трансформы: ping и баланс аккаунта funstat."""

from __future__ import annotations

from .. import entities as E
from ..helpers import FunstatTransform, UIM_INFORM


class FunstatPing(FunstatTransform):
    """funstat.ping() — проверка доступности API. Вход: любая сущность."""

    input_entity = E.PHRASE

    @classmethod
    def run(cls, fs, request, response):
        res = fs.ping()
        if res is None:
            response.addUIMessage("Ping не вернул данных.", UIM_INFORM)
            return
        ent = response.addEntity(E.PHRASE, f"funstat ping: {res.responce_ping} ms")
        ent.addProperty("funstat.request_ping", "Request ping", "loose", str(res.request_ping))
        ent.addProperty("funstat.response_ping", "Response ping", "loose", str(res.responce_ping))
        ent.addDisplayInformation(
            f"request_ping: {res.request_ping}<br/>responce_ping: {res.responce_ping}",
            "Funstat ping",
        )


class FunstatBalance(FunstatTransform):
    """funstat.get_balance() — текущий баланс и стоимость запроса."""

    input_entity = E.PHRASE

    @classmethod
    def run(cls, fs, request, response):
        res = fs.get_balance()
        if res is None:
            response.addUIMessage("Баланс не получен.", UIM_INFORM)
            return
        ent = response.addEntity(E.PHRASE, f"funstat balance: {res.current_ballance}")
        ent.addProperty("funstat.balance", "Balance", "loose", str(res.current_ballance))
        ent.addProperty("funstat.request_cost", "Request cost", "loose", str(res.request_cost))
        ent.addProperty("funstat.request_duration", "Duration", "loose", str(res.request_duration))
        ent.addDisplayInformation(
            f"Balance: {res.current_ballance}<br/>"
            f"Request cost: {res.request_cost}<br/>"
            f"Duration: {res.request_duration}",
            "Funstat balance",
        )
