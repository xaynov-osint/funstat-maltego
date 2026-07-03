"""Константы типов сущностей Maltego, используемых трансформами funstat.

Кастомные типы (``funstat.*``) Maltego автоматически создаёт как placeholder
при первом возврате локальной трансформой. При желании их можно оформить
полноценно через Entity Manager (см. MALTEGO_SETUP.md).
"""

# --- сущности ---
# Пользователь Telegram — используем ВСТРОЕННУЮ сущность Maltego (иконка,
# нативные поля affiliation.uid / person.name, цепочки трансформ).
TG_USER = "maltego.affiliation.Telegram"

# Тип(ы) входных сущностей, на которых должны появляться пользовательские
# трансформы (context menu). Используется билдером mtz.
USER_INPUT_ENTITIES = ["maltego.Phrase", "maltego.affiliation.Telegram"]

# --- остальные кастомные сущности funstat ---
TG_GROUP = "funstat.TelegramGroup"        # value = title или id группы/канала
TG_MESSAGE = "funstat.TelegramMessage"    # value = текст/фрагмент сообщения
TG_STICKER = "funstat.TelegramSticker"    # value = короткое имя стикерпака
TG_USERNAME = "funstat.TelegramUsername"  # value = @username (историческое имя)

# --- встроенные сущности Maltego ---
PHRASE = "maltego.Phrase"                  # скалярные результаты (счётчики, ping, баланс)
PERSON_NAME = "maltego.Phrase"             # отображаемое имя пользователя
