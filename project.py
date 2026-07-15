"""maltego-trx entry point for the funstat transforms.

Run a single transform locally (Maltego feeds XML to stdin):
    python project.py local FunstatStats

List the available transforms:
    python project.py list

TDS/iTDS server mode (requires flask; not needed for local transforms):
    python project.py runserver
"""

import sys

# Force UTF-8 for output: Maltego reads the transform result as UTF-8,
# while Python on Windows prints in the console codepage (cp1251) by default,
# which turns Cyrillic into "?". Must come before any output.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

from maltego_trx.registry import register_transform_function
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.handler import handle_run

# Import the transforms package. Register each DiscoverableTransform subclass
# explicitly (the project has several classes per module, so the
# register_transform_classes auto-walk doesn't fit here).
from funstat_maltego import transforms

for _name in transforms.__all__:
    _cls = getattr(transforms, _name)
    if isinstance(_cls, type) and issubclass(_cls, DiscoverableTransform):
        register_transform_function(_cls)

# The Flask app is only needed for runserver; not required for local mode.
try:
    from maltego_trx.server import app
except Exception:  # noqa: BLE001
    app = None


def _list_transforms():
    from maltego_trx.registry import mapping

    print("Registered funstat transforms:")
    for name in sorted(mapping):
        print(f"  - {name}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        _list_transforms()
    else:
        handle_run(__name__, sys.argv, app)
