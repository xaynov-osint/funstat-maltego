"""Фабрика клиента funstat-api.

Токен берётся в таком порядке приоритета:
    1) жёстко прописанная заглушка ``API_TOKEN`` (для быстрой отладки);
    2) переменная окружения ``FUNSTAT_API_TOKEN``;
    3) файл ``.env`` в корне проекта (строка ``FUNSTAT_API_TOKEN=...``).

Клиент ``FunstatClient`` является контекст-менеджером, поэтому используйте его так:

    from funstat_maltego.client import open_client
    with open_client() as fs:
        resp = fs.stats("durov")
"""

from __future__ import annotations

import os

# --------------------------------------------------------------------------- #
# ЗАГЛУШКА ДЛЯ ТОКЕНА.
# По умолчанию None — токен берётся из .env / переменной окружения (рекомендуется).
# Можно вписать токен прямо сюда, если так удобнее при отладке:
#
# API_TOKEN = "ЗАГЛУШКА_ТОКЕНА"
# --------------------------------------------------------------------------- #
API_TOKEN: str | None = None

ENV_VAR = "FUNSTAT_API_TOKEN"

# Корень проекта = папка на уровень выше этого пакета (там лежит .env).
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FunstatTokenError(RuntimeError):
    """Токен не найден / не задан."""


class FunstatDependencyError(RuntimeError):
    """Библиотека funstat-api не установлена в окружении."""


def _load_dotenv() -> None:
    """Минимальный загрузчик .env без внешних зависимостей.

    Читает ``<корень проекта>/.env`` и переносит значения в os.environ,
    НЕ перетирая уже заданные переменные окружения. Формат: ``KEY=VALUE``,
    строки с ``#`` и пустые игнорируются, кавычки вокруг значения снимаются.
    """
    path = os.path.join(_PROJECT_ROOT, ".env")
    if not os.path.isfile(path):
        return
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        pass


def get_token() -> str:
    """Вернуть токен или бросить :class:`FunstatTokenError`."""
    if API_TOKEN:
        return API_TOKEN
    _load_dotenv()
    token = os.environ.get(ENV_VAR)
    if not token:
        raise FunstatTokenError(
            f"Токен funstat-api не задан. Укажите его одним из способов: "
            f"файл .env со строкой {ENV_VAR}=..., переменная окружения {ENV_VAR}, "
            f"или API_TOKEN в funstat_maltego/client.py."
        )
    return token


def open_client():
    """Создать и вернуть экземпляр ``FunstatClient`` (контекст-менеджер).

    Импорт библиотеки выполняется лениво, чтобы отсутствие пакета
    приводило к аккуратной ошибке (UIMessage), а не к падению всей трансформы.
    """
    try:
        from funstat_api import FunstatClient  # type: ignore
    except ImportError as exc:  # pragma: no cover - зависит от окружения
        raise FunstatDependencyError(
            "Библиотека funstat-api не установлена. "
            "Выполните: pip install funstat-api"
        ) from exc

    return FunstatClient(get_token())
