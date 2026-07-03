"""Экспорт всех трансформ funstat для авторегистрации в maltego-trx.

``register_transform_classes(transforms)`` в project.py пройдётся по атрибутам
этого пакета и подхватит все классы-наследники DiscoverableTransform.
"""

from .utility import FunstatPing, FunstatBalance
from .user_identity import (
    FunstatResolveUsername,
    FunstatBasicInfo,
    FunstatGetNames,
    FunstatGetUsernames,
    FunstatUsernameUsage,
)
from .user_stats import (
    FunstatStats,
    FunstatStatsMin,
    FunstatMessagesCount,
    FunstatGroupsCount,
    FunstatReputation,
)
from .user_activity import (
    FunstatGetMessages,
    FunstatGetChats,
    FunstatCommonGroups,
    FunstatGetStickers,
    FunstatGetGifts,
    FunstatSearchText,
)
from .groups import (
    FunstatGroupInfo,
    FunstatGroupMembers,
    FunstatCommonGroupsForUsers,
)

__all__ = [
    # utility
    "FunstatPing",
    "FunstatBalance",
    # identity
    "FunstatResolveUsername",
    "FunstatBasicInfo",
    "FunstatGetNames",
    "FunstatGetUsernames",
    "FunstatUsernameUsage",
    # stats
    "FunstatStats",
    "FunstatStatsMin",
    "FunstatMessagesCount",
    "FunstatGroupsCount",
    "FunstatReputation",
    # activity
    "FunstatGetMessages",
    "FunstatGetChats",
    "FunstatCommonGroups",
    "FunstatGetStickers",
    "FunstatGetGifts",
    "FunstatSearchText",
    # groups
    "FunstatGroupInfo",
    "FunstatGroupMembers",
    "FunstatCommonGroupsForUsers",
]
