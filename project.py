"""Точка входа maltego-trx для трансформ funstat.

Локальный запуск одной трансформы (Maltego подаёт XML на stdin):
    python project.py local FunstatStats

Список доступных трансформ:
    python project.py list

Режим TDS/iTDS-сервера (требует flask; не обязателен для локальных трансформ):
    python project.py runserver
"""

import sys

# Форсируем UTF-8 для вывода: Maltego читает результат трансформы как UTF-8,
# а Python на Windows по умолчанию печатает в кодировке консоли (cp1251),
# из-за чего кириллица превращается в "?". Должно стоять до любого вывода.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

from maltego_trx.registry import register_transform_function
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.handler import handle_run

# Импорт пакета с трансформами. Регистрируем каждый класс-наследник
# DiscoverableTransform явно (в проекте несколько классов на модуль, поэтому
# авто-обход register_transform_classes здесь не подходит).
from funstat_maltego import transforms

for _name in transforms.__all__:
    _cls = getattr(transforms, _name)
    if isinstance(_cls, type) and issubclass(_cls, DiscoverableTransform):
        register_transform_function(_cls)

# Flask-приложение нужно только для runserver; для local-режима не обязательно.
try:
    from maltego_trx.server import app
except Exception:  # noqa: BLE001
    app = None


def _list_transforms():
    from maltego_trx.registry import mapping

    print("Зарегистрированные трансформы funstat:")
    for name in sorted(mapping):
        print(f"  - {name}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        _list_transforms()
    else:
        handle_run(__name__, sys.argv, app)
