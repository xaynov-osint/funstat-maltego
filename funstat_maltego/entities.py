"""Constants for the Maltego entity types used by the funstat transforms.

Custom types (``funstat.*``) are created automatically by Maltego as placeholders
the first time a local transform returns them. If desired, they can be defined
properly via the Entity Manager (see MALTEGO_SETUP.md).
"""

# --- entities ---
# Telegram user — we use the BUILT-IN Maltego entity (icon, native
# affiliation.uid / person.name fields, transform chaining).
TG_USER = "maltego.affiliation.Telegram"

# Input entity type(s) on which the custom transforms should appear
# (context menu). Used by the mtz builder.
USER_INPUT_ENTITIES = ["maltego.Phrase", "maltego.affiliation.Telegram"]

# --- other custom funstat entities ---
TG_GROUP = "funstat.TelegramGroup"        # value = title or id of the group/channel
TG_MESSAGE = "funstat.TelegramMessage"    # value = message text/fragment
TG_STICKER = "funstat.TelegramSticker"    # value = sticker pack short name
TG_USERNAME = "funstat.TelegramUsername"  # value = @username (historical name)

# --- built-in Maltego entities ---
PHRASE = "maltego.Phrase"                  # scalar results (counters, ping, balance)
PERSON_NAME = "maltego.Phrase"             # user's display name
