#!/usr/bin/env python3
"""Synchronize both main README mod tables with downloaded JARs.

Preserves manually curated archive rows and historical mod-existence statuses.
Only marks a version available when an actual JAR is present.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
manifest = json.loads((ROOT / "RECOVERED-SOURCES.json").read_text())
coverage = json.loads((ROOT / "MC-VERSION-COVERAGE.json").read_text())
notes = json.loads((ROOT / "MOD-EXISTENCE-NOTES.json").read_text())
early = notes.get("early_versions", [])
versions = list(dict.fromkeys([x["minecraft_version"] for x in coverage["records"]] + early))
files = [x for x in manifest.get("files", []) if (ROOT / x["path"]).is_file()]
def key(version):
    if re.fullmatch(r"(?:1|26)\.\d+(?:\.\d+)?", version):
        return (2, *[int(n) for n in version.split(".")])
    return (0, version)
def version_from_row(row):
    return row.split("|")[1].strip().replace(" (inferred)", "")
def status(version, found):
    if found:
        return "🟢 Yes — archived build"
    if version in early or re.fullmatch(r"1\.(?:[0-9]|10|11)(?:\.\d+)?", version):
        return "⚫ No — predates documented mod support"
    return "🟡 Unknown — no verified build"

readme = README.read_text()
start = readme.index("## Downloads by mod")
end = readme.index("## Minecraft Java releases", start)
section = readme[start:end]
for heading, next_heading, mod in [
    ("### Meteor Client", "### Baritone", "meteor"),
    ("### Baritone", None, "baritone"),
]:
    a = section.index(heading)
    b = section.index(next_heading, a + len(heading)) if next_heading else len(section)
    chunk = section[a:b]
    lines = chunk.splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith("| Minecraft version |"))
    old = [line for line in lines[header+2:] if line.startswith("|") and not line.startswith("|---")]
    # Preserve pre-existing non-generated archive rows, but discard stale missing
    # and generated recovered rows before rebuilding from actual files.
    original = [
        line for line in old
        if "**Missing**" not in line
        and "source/" not in line
    ]
    by_version = {}
    for line in original:
        by_version.setdefault(version_from_row(line), []).append(line)
    recovered = {}
    for item in files:
        path = item["path"]
        parts = path.split("/")
        if len(parts) < 6 or parts[2] != mod or not path.endswith(".jar"):
            continue
        version, loader, filename = parts[4], parts[3], parts[-1]
        source = parts[1]
        # The build filename is not necessarily an independently verified mod version.
        line = (
            f"| {version} | 🟢 Yes — archived build | {loader} | "
            f"{filename[:-4]} (filename) | [{source}]({item['source_url']}) | "
            f"[⬇️ Download JAR]({path}) |"
        )
        recovered.setdefault(version, []).append(line)
    all_versions = sorted(set(versions) | set(by_version) | set(recovered), key=key, reverse=True)
    rows = []
    for version in all_versions:
        existing = by_version.get(version, [])
        downloaded = recovered.get(version, [])
        for line in existing:
            cells = line.split("|")
            if len(cells) == 7:
                cells[2] = " " + status(version, True) + " "
            elif len(cells) == 6:
                cells.insert(2, " " + status(version, True) + " ")
            rows.append("|".join(cells))
        rows.extend(downloaded)
        if not existing and not downloaded:
            rows.append(f"| {version} | {status(version, False)} | — | 🔴 **Missing** | — | 🔴 **Missing** |")
    prefix = "\n".join(lines[:header])
    replacement = prefix + "\n| Minecraft version | Mod existed? | Loader | Mod version | Archive found in | Download |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n"
    section = section[:a] + replacement + section[b:]
readme = readme[:start] + section + readme[end:]
README.write_text(readme)
print("Updated main README tables from", len(files), "verified-present recovered JAR paths")
