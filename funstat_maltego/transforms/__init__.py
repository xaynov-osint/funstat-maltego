"""Export of all funstat transforms for auto-registration in maltego-trx.

``register_transform_classes(transforms)`` in project.py walks the attributes
of this package and picks up all DiscoverableTransform subclasses.
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
