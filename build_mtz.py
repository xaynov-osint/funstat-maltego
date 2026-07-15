"""Generator for the Maltego config archive (.mtz) with all funstat transforms.

Run:
    python build_mtz.py

Result: funstat_maltego.mtz — imported via
Maltego → Import → Import Configuration (.mtz).

All transforms are registered under the local "Local" server, input = maltego.Phrase
(universal: the entity value = ID / @username / group). Command/paths are taken
from the constants below — adjust them if your Python or project path differs.
"""

from __future__ import annotations

import os
import sys
import zipfile
from xml.sax.saxutils import escape

# Paths are detected automatically from the current interpreter and this file's location.
# If needed, they can be overridden via the environment variables
# FUNSTAT_PYTHON_EXE / FUNSTAT_PROJECT_DIR.
PYTHON_EXE = os.environ.get("FUNSTAT_PYTHON_EXE", sys.executable)
PROJECT_DIR = os.environ.get(
    "FUNSTAT_PROJECT_DIR", os.path.dirname(os.path.abspath(__file__))
)
PROJECT_PY = os.path.join(PROJECT_DIR, "project.py")
SET_NAME = "Funstat"
# Input entities: a plain phrase + Maltego's built-in Telegram entity.
# The transforms will be available via right-click on both.
INPUT_ENTITIES = ["maltego.Phrase", "maltego.affiliation.Telegram"]

# (transform_id, display_name, class_name, description)
TRANSFORMS = [
    ("funstat.ping", "Funstat: Ping", "FunstatPing", "Check API availability"),
    ("funstat.balance", "Funstat: Balance", "FunstatBalance", "Balance and request cost"),
    ("funstat.resolveusername", "Funstat: Resolve username", "FunstatResolveUsername", "@username -> users"),
    ("funstat.basicinfo", "Funstat: Basic info", "FunstatBasicInfo", "Basic info by ID"),
    ("funstat.statsmin", "Funstat: Stats (min)", "FunstatStatsMin", "Brief statistics"),
    ("funstat.stats", "Funstat: Stats", "FunstatStats", "Full statistics"),
    ("funstat.messagescount", "Funstat: Messages count", "FunstatMessagesCount", "Number of messages"),
    ("funstat.groupscount", "Funstat: Groups count", "FunstatGroupsCount", "Number of groups"),
    ("funstat.getmessages", "Funstat: Messages", "FunstatGetMessages", "User's messages"),
    ("funstat.getchats", "Funstat: Chats", "FunstatGetChats", "User's chats/groups"),
    ("funstat.getnames", "Funstat: Names history", "FunstatGetNames", "Name history"),
    ("funstat.getusernames", "Funstat: Usernames history", "FunstatGetUsernames", "Username history"),
    ("funstat.reputation", "Funstat: Reputation", "FunstatReputation", "Reputation"),
    ("funstat.commongroups", "Funstat: Common groups", "FunstatCommonGroups", "Users with common groups"),
    ("funstat.getstickers", "Funstat: Stickers", "FunstatGetStickers", "Sticker packs"),
    ("funstat.getgifts", "Funstat: Gifts", "FunstatGetGifts", "Gifts"),
    ("funstat.usernameusage", "Funstat: Username usage", "FunstatUsernameUsage", "Who uses a @username"),
    ("funstat.commongroupsforusers", "Funstat: Common groups (multi)", "FunstatCommonGroupsForUsers", "Common groups for a set of ids"),
    ("funstat.groupinfo", "Funstat: Group info", "FunstatGroupInfo", "Group/channel card"),
    ("funstat.groupmembers", "Funstat: Group members", "FunstatGroupMembers", "Group members"),
    ("funstat.searchtext", "Funstat: Search text", "FunstatSearchText", "Who wrote a text and where"),
]


def _input_constraints() -> str:
    return "\n".join(
        f'      <Entity type="{escape(e)}" min="1" max="1"/>' for e in INPUT_ENTITIES
    )


def transform_xml(tid: str, display: str, desc: str) -> str:
    return f"""<MaltegoTransform name="{escape(tid)}" displayName="{escape(display)}" abstract="false" template="false" visibility="public" description="{escape(desc)}" author="funstat_maltego" requireDisplayInfo="false">
   <TransformAdapter>com.paterva.maltego.transform.protocol.v2api.LocalTransformAdapterV2</TransformAdapter>
   <Properties>
      <Fields>
         <Property name="transform.local.command" type="string" nullable="false" hidden="false" readonly="false" description="The command to execute for this transform" popup="false" abstract="false" visibility="public" auth="false" displayName="Command line">
            <SampleValue></SampleValue>
         </Property>
         <Property name="transform.local.parameters" type="string" nullable="true" hidden="false" readonly="false" description="The parameters to pass to the transform command" popup="false" abstract="false" visibility="public" auth="false" displayName="Command parameters">
            <SampleValue></SampleValue>
         </Property>
         <Property name="transform.local.working-directory" type="string" nullable="true" hidden="false" readonly="false" description="The working directory used when invoking the executable" popup="false" abstract="false" visibility="public" auth="false" displayName="Working directory">
            <SampleValue>/</SampleValue>
         </Property>
         <Property name="transform.local.debug" type="boolean" nullable="true" hidden="false" readonly="false" description="When set, the transform's text output will be printed to the output window" popup="false" abstract="false" visibility="public" auth="false" displayName="Show debug info">
            <SampleValue>false</SampleValue>
         </Property>
      </Fields>
   </Properties>
   <InputConstraints>
{_input_constraints()}
   </InputConstraints>
   <OutputEntities/>
   <defaultSets>
      <Set name="{escape(SET_NAME)}"/>
   </defaultSets>
   <StealthLevel>0</StealthLevel>
</MaltegoTransform>
"""


def settings_xml(cls: str) -> str:
    params = f"{PROJECT_PY} local {cls}"
    return f"""<TransformSettings enabled="true" disclaimerAccepted="false" showHelp="true" runWithAll="false" favorite="false">
   <Properties>
      <Property name="transform.local.command" type="string" popup="false">{escape(PYTHON_EXE)}</Property>
      <Property name="transform.local.parameters" type="string" popup="false">{escape(params)}</Property>
      <Property name="transform.local.working-directory" type="string" popup="false">{escape(PROJECT_DIR)}</Property>
      <Property name="transform.local.debug" type="boolean" popup="false">false</Property>
   </Properties>
</TransformSettings>
"""


def server_tas() -> str:
    rows = "\n".join(f'      <Transform name="{escape(tid)}"/>' for tid, *_ in TRANSFORMS)
    return f"""<MaltegoServer name="Local" enabled="true" description="Local transforms hosted on this machine" url="http://localhost">
   <LastSync>2026-07-04 00:00:00.000 UTC</LastSync>
   <Protocol version="0.0"/>
   <Authentication type="none"/>
   <Transforms>
{rows}
   </Transforms>
   <Seeds/>
</MaltegoServer>
"""


def set_xml() -> str:
    rows = "\n".join(f'      <Transform name="{escape(tid)}"/>' for tid, *_ in TRANSFORMS)
    return f"""<TransformSet name="{escape(SET_NAME)}" description="Funstat Telegram OSINT transforms">
   <Transforms>
{rows}
   </Transforms>
</TransformSet>
"""


def version_props() -> str:
    return "maltego.client.version=4.6.0\nmaltego.client.subtitle=\nmaltego.pandora.version=1.4.2\n"


def main() -> None:
    out = "funstat_maltego.mtz"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("version.properties", version_props())
        z.writestr("Servers/Local.tas", server_tas())
        z.writestr(f"TransformSets/{SET_NAME}.set", set_xml())
        for tid, display, cls, desc in TRANSFORMS:
            z.writestr(f"TransformRepositories/Local/{tid}.transform", transform_xml(tid, display, desc))
            z.writestr(f"TransformRepositories/Local/{tid}.transformsettings", settings_xml(cls))
    print(f"OK: {out} ({len(TRANSFORMS)} transforms)")
    print("Detected paths (for manual setup in Maltego):")
    print(f"  Command line      : {PYTHON_EXE}")
    print(f"  Working directory : {PROJECT_DIR}")
    print(f"  Parameters (template): {PROJECT_PY} local <ClassName>")


if __name__ == "__main__":
    main()
