# funstat-maltego

![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Transforms](https://img.shields.io/badge/transforms-21-orange)
![Maltego](https://img.shields.io/badge/Maltego-local%20transforms-purple?logo=maltego)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![GitHub stars](https://img.shields.io/github/stars/xaynov-osint/funstat-maltego?style=social)
![GitHub issues](https://img.shields.io/github/issues/xaynov-osint/funstat-maltego)


A set of local transforms for [Maltego](https://www.maltego.com/) built on top of the [`funstat-api`](https://pypi.org/project/funstat-api/) library — Telegram OSINT statistics (names, usernames, groups, messages, reputation, etc.) directly in the Maltego graph.

All **21 methods** of the library are implemented as separate transforms using the official [`maltego-trx`](https://github.com/paterva/maltego-trx) framework.

---

## Features

| Transform | API Method | Description |
|---|---|---|
| Funstat: Ping | `ping` | Check API availability |
| Funstat: Balance | `get_balance` | Balance and request cost |
| Funstat: Resolve username | `resolve_username` | `@username` → user(s) |
| Funstat: Basic info | `basic_info_by_id` | Basic info by ID (supports list) |
| Funstat: Stats | `stats` | Full user statistics |
| Funstat: Stats (min) | `stats_min` | Brief statistics |
| Funstat: Messages count | `messages_count` | Number of messages |
| Funstat: Groups count | `groups_count` | Number of groups |
| Funstat: Messages | `get_messages` | Messages (+ groups) |
| Funstat: Chats | `get_chats` | User chats/groups |
| Funstat: Names history | `get_names` | Display name history |
| Funstat: Usernames history | `get_usernames` | Username history |
| Funstat: Reputation | `rep` | Reputation |
| Funstat: Common groups | `common_groups` | Users with common groups |
| Funstat: Stickers | `get_stickers` | Sticker packs |
| Funstat: Gifts | `get_gifts` | Gifts (senders/recipients) |
| Funstat: Username usage | `username_usage` | Who/what is using a username |
| Funstat: Common groups (multi) | `common_groups_for_users` | Common groups for a set of IDs |
| Funstat: Group info | `get_group_info` | Group/channel card + statistics |
| Funstat: Group members | `get_group_members` | Group members |
| Funstat: Search text | `search_text` | Who wrote a given text and where |

Users are returned as the built-in `maltego.affiliation.Telegram` entity (with the `affiliation.uid` field), so transforms **chain together**: search/members/gifts → users → their stats/names/usernames, etc.

---

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/xaynov-osint/funstat-maltego
cd funstat-maltego
python -m pip install -r requirements.txt
```

Dependencies: `funstat-api`, `maltego-trx`.

## Token Setup

First, send the `/api` command inside any working mirror, then copy the token for use with the transform.

The `funstat-api` token is resolved in the following priority order:

1. `API_TOKEN` in `funstat_maltego/client.py` (for quick debugging);
2. The `FUNSTAT_API_TOKEN` environment variable;
3. A `.env` file in the project root (**recommended**).

Copy the template and enter your token:

```bash
cp .env.example .env
# .env:
# FUNSTAT_API_TOKEN=your_token
```

`.env` is already in `.gitignore` and will not be committed to the repository.

---

## Connecting to Maltego

### Option A — Import a ready-made config (recommended)

```bash
python build_mtz.py
```

The script will build `funstat_maltego.mtz` (Python and project paths are detected automatically) and print them for reference.

Then in Maltego: **Import → Import Configuration** → select `funstat_maltego.mtz` → check all → **Finish**.

All 21 transforms will appear in the **Funstat** set under the **Local** server. Input entities are `maltego.Phrase` and `maltego.affiliation.Telegram`.

### Option B — Manual setup

Register each transform via **Transforms → New Local Transform**. Run `python build_mtz.py` first — it prints the exact `Command line`, `Working directory` and `Parameters` for your machine. Then, per transform:

- **Command line**: your Python executable (printed by the script)
- **Parameters**: `<project_dir>/project.py local <ClassName>` (e.g. `FunstatStats`)
- **Working directory**: the project directory
- **Input entity type**: `maltego.Phrase` (universal) or `maltego.affiliation.Telegram`

Class names match the `Funstat*` transforms — list them with `python project.py list`.

---

## Usage

1. Drop a `maltego.affiliation.Telegram` entity onto the graph with a value — an ID, `@username`, or (for group transforms) a group.
2. Right-click → **Run Transforms** → **Funstat** set → select the desired transform.

Notes:
- `Resolve username` / `Username usage` work **only with `@username`**.
- `Basic info` and most user transforms accept both IDs and usernames (resolved on the API side). When run from a Telegram entity, the identifier is taken from `affiliation.uid`.
- The Maltego results slider (Slider) sets the limit for `Messages`, `Gifts`, and `Search text`.

---

## Project Structure

```
├─ project.py               # maltego-trx entry point (local / list / runserver)
├─ build_mtz.py             # builds the importable .mtz (paths auto-detected)
├─ requirements.txt
├─ .env.example             # token template
└─ funstat_maltego/
   ├─ client.py             # client factory + .env loading
   ├─ entities.py           # Maltego entity types
   ├─ helpers.py            # base class, error handling, entity builders
   └─ transforms/           # 21 transform classes, grouped by topic
```

## Error Handling

All calls are wrapped: if the token is missing, the library is unavailable, or the API returns an error (including `403 User Hidden Data`), the transform **does not crash** — it returns a `UIMessage` to the Maltego interface instead.

---

## Disclaimer

This tool is intended for legal OSINT, authorized testing, and educational purposes. Compliance with applicable laws, the service's Terms of Service, and the privacy of third parties is the sole responsibility of the user.
