"""funstat-api client factory.

The token is resolved in the following priority order:
    1) the hard-coded ``API_TOKEN`` stub (for quick debugging);
    2) the ``FUNSTAT_API_TOKEN`` environment variable;
    3) the ``.env`` file in the project root (line ``FUNSTAT_API_TOKEN=...``).

The ``FunstatClient`` is a context manager, so use it like this:

    from funstat_maltego.client import open_client
    with open_client() as fs:
        resp = fs.stats("durov")
"""

from __future__ import annotations

import os

# --------------------------------------------------------------------------- #
# TOKEN STUB.
# Defaults to None — the token is taken from .env / an environment variable (recommended).
# You can hard-code the token right here if that's more convenient for debugging:
#
# API_TOKEN = "TOKEN_STUB"
# --------------------------------------------------------------------------- #
API_TOKEN: str | None = None

ENV_VAR = "FUNSTAT_API_TOKEN"

# Project root = the folder one level above this package (that's where .env lives).
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FunstatTokenError(RuntimeError):
    """Token not found / not set."""


class FunstatDependencyError(RuntimeError):
    """The funstat-api library is not installed in the environment."""


def _load_dotenv() -> None:
    """Minimal .env loader without external dependencies.

    Reads ``<project root>/.env`` and copies the values into os.environ,
    WITHOUT overwriting already-set environment variables. Format: ``KEY=VALUE``,
    lines with ``#`` and empty lines are ignored, surrounding quotes are stripped.
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
    """Return the token or raise :class:`FunstatTokenError`."""
    if API_TOKEN:
        return API_TOKEN
    _load_dotenv()
    token = os.environ.get(ENV_VAR)
    if not token:
        raise FunstatTokenError(
            f"The funstat-api token is not set. Provide it one of these ways: "
            f"a .env file with the line {ENV_VAR}=..., the {ENV_VAR} environment variable, "
            f"or API_TOKEN in funstat_maltego/client.py."
        )
    return token


def open_client():
    """Create and return a ``FunstatClient`` instance (context manager).

    The library is imported lazily so that a missing package results in a
    clean error (UIMessage) rather than crashing the whole transform.
    """
    try:
        from funstat_api import FunstatClient  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise FunstatDependencyError(
            "The funstat-api library is not installed. "
            "Run: pip install funstat-api"
        ) from exc

    return FunstatClient(get_token())
