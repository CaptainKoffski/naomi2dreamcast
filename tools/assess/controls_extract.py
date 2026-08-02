#!/usr/bin/env python3
"""Parse MAME's naomi.cpp GAME() rows -> per-set identity/input JSON on stdout.
Pinned source: ../cleopatra/tools/mame (commit 59e7c0b). Override: env MAME_NAOMI."""
import json, os, re, sys

# GAME( 1999, set, parent, machine, input, class, init, rot, "Maker", "Title", flags )
_GAME = re.compile(
    r'GAME\(\s*(\d{4}),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*\w+,\s*\w+,\s*\w+,\s*'
    r'"([^"]*)",\s*"([^"]*)",\s*([^)]*)\)', re.S)

# INPUT_PORTS name -> spec §4.4 ladder class. Filled from:
#   grep -o 'INPUT_PORTS_START( *[a-z0-9_]*' naomi.cpp
# "review" = hint unknown; the assessing agent must research + set the class by hand.
DEVICE_HINTS = {
    "naomi": "stick",             # 2p joystick + 6 buttons, the default panel
    "naomi_mie": "review",        # base fragment: system/DIP/EEPROM bits only, no player controls; never used as a GAME's own input_ports value
    "marstv": "stick",            # renamed BUTTON1-3 only, no joystick -- plain 3-button quiz panel
    "hotd2": "dc_peripheral",     # IPT_LIGHTGUN_X/Y -- light gun; DC light gun exists
    "crzytaxi": "dc_peripheral",  # IPT_PADDLE steering + 2x IPT_PEDAL -- wheel-type driving control
    "dybbnao": "stick",           # 2-axis AD_STICK + 1 PEDAL per player -- maps onto DC pad's stick + analog trigger
    "zombrvn": "stick",           # AD_STICK_X/Y + up to 3 buttons per player -- standard analog-stick control
    "jambo": "dc_peripheral",     # IPT_PADDLE + 2x IPT_PEDAL -- wheel/pedal driving scheme
    "18wheelr": "dc_peripheral",  # IPT_PADDLE + 2x IPT_PEDAL -- truck sim, wheel + pedals
    "alpilota": "awkward",        # yoke (2-axis) + rudder pedal (3rd axis) + 2 independent thrust levers = 5 analog channels; DC pad exposes only 4 (stick X/Y + 2 triggers)
    "sstrkfgt": "awkward",        # derived from alpilota, same yoke/rudder/dual-throttle axis-count problem
    "crackndj": "review",         # only a single "Fader" axis + Start defined; no turntable/mixer buttons represented here, real control surface unclear
    "monkeyba": "stick",          # pure 2-axis AD_STICK tilt control, no buttons besides Start -- maps 1:1 onto DC's analog stick
    "shaktamb": "review",         # Knock/Shake L/Shake R/Up/Down imply a physical tambourine controller; no DC tambourine peripheral, unclear if plain buttons preserve playability
    "naomi_mp": "pad_adaptable",  # JVS mahjong panel (IPT_MAHJONG_*)
    "suchie3": "pad_adaptable",   # mahjong panel, same as naomi_mp with a swapped key-matrix read function
    "naomi_kb": "dc_peripheral",  # IPT_KEYBOARD ports -- DC keyboard peripheral exists
}


def default_mame_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.environ.get("MAME_NAOMI", os.path.normpath(os.path.join(
        here, "../../..", "cleopatra/tools/mame/src/mame/sega/naomi.cpp")))


def extract(text):
    matches = [m.groups() for m in _GAME.finditer(text)]
    # BIOS placeholders (e.g. "naomi", "naomigd") show up as the `parent` of
    # otherwise-standalone games (MAME clones GD-ROM/cart titles off their BIOS
    # for ROM-sharing bookkeeping, not because they're really a clone of another
    # game) -- collapse those references to None, same as parent == "0".
    bios_roots = {setname for _, setname, _, _, _, _, _, flags in matches
                  if "MACHINE_IS_BIOS_ROOT" in flags}
    rows = {}
    for year, setname, parent, machine, inp, maker, title, flags in matches:
        if "MACHINE_IS_BIOS_ROOT" in flags:
            continue
        rows[setname] = {
            "year": year,
            "parent": None if parent == "0" or parent in bios_roots else parent,
            "machine": machine,
            "input_ports": inp,
            "maker": maker,
            "title": title,
            "not_working": "MACHINE_NOT_WORKING" in flags,
            "device_class_hint": DEVICE_HINTS.get(inp, "review"),
        }
    return rows


if __name__ == "__main__":
    with open(default_mame_path(), encoding="utf-8", errors="replace") as fh:
        print(json.dumps(extract(fh.read()), indent=2, sort_keys=True))
