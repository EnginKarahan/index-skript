#!/usr/bin/env python3

import os
import re
import yaml

arbeitsverzeichnis = os.getcwd()
index_md_path = os.path.join(arbeitsverzeichnis, "Index.md")

def get_md_files():
    return sorted([f for f in os.listdir(arbeitsverzeichnis)
                   if f.endswith(".md") and f != "Index.md"])

def parse_yaml_header(filepath):
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()
    if not lines or lines[0].strip() != "---":
        return {}
    yaml_lines = []
    for line in lines[1:]:
        if line.strip() == "---" or line.strip() == "...":
            break
        yaml_lines.append(line)
    try:
        return yaml.safe_load("".join(yaml_lines))
    except Exception:
        return {}

def get_title_from_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("# ").strip()
    return os.path.splitext(os.path.basename(filepath))[0]

def parse_index_entries(index_lines):
    eintraege = set()
    link_re = re.compile(r"\[\[([^\]]+)\]\]")
    for line in index_lines:
        for match in link_re.finditer(line):
            eintraege.add(match.group(1))
    return eintraege

def find_section_indices(lines):
    indices = {}
    for i, line in enumerate(lines):
        m = re.match(r"^## ([A-ZÄÖÜ])\s*$", line)
        if m:
            indices[m.group(1)] = i
    return indices

def insert_entry(lines, section_indices, entry_key, entry_line):
    key = entry_key.upper()
    if key not in section_indices:
        # Neue Sektion einfügen (sollte durch Vorlage nicht nötig sein)
        keys = sorted(list(section_indices.keys()) + [key])
        pos = keys.index(key)
        if pos == 0:
            insert_at = max(section_indices.values()) + 1
        else:
            prev_section = keys[pos - 1]
            prev_idx = section_indices[prev_section]
            insert_at = prev_idx + 1
            while insert_at < len(lines) and not lines[insert_at].startswith("## "):
                insert_at += 1
        lines.insert(insert_at, f"## {key}\n")
        lines.insert(insert_at + 1, entry_line)
        return

    idx = section_indices[key] + 1
    end_idx = idx
    while end_idx < len(lines) and not lines[end_idx].startswith("## "):
        end_idx += 1
    sublines = lines[idx:end_idx]
    titles = [(i, l) for i, l in enumerate(sublines) if l.strip()]
    insert_pos = None
    new_title = entry_line.split("]] ")[-1].strip()
    for i, l in titles:
        existing_title = l.split("]] ")[-1].strip()
        if new_title < existing_title:
            insert_pos = idx + i
            break
    if insert_pos is None:
        insert_pos = end_idx
    lines.insert(insert_pos, entry_line)

def create_empty_index_md():
    header = '''---
title: "Index"
author:
  - 
date: 
keywords: 
    - Index
    - Zettelkasten
    - Wissensmangement
ID: 
    - 
...

# Index

'''
    # Alle Buchstaben-Sektionen (A-Z, Umlaute auf Wunsch ergänzen)
    sections = [f"## {chr(i)}\n\n" for i in range(ord('A'), ord('Z')+1)]
    # Bei Bedarf auch ## Ä, Ö, Ü ergänzen:
    sections += ["## Ä\n\n", "## Ö\n\n", "## Ü\n\n"]
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.writelines(sections)
    print("Leere Index.md mit allen Buchstabenüberschriften angelegt.")

def main():
    if not os.path.exists(index_md_path):
        create_empty_index_md()

    with open(index_md_path, encoding="utf-8") as f:
        index_lines = f.readlines()

    bestehende_eintraege = parse_index_entries(index_lines)
    section_indices = find_section_indices(index_lines)

    md_files = get_md_files()
    neue_eintraege = []

    for mdfile in md_files:
        filepath = os.path.join(arbeitsverzeichnis, mdfile)
        yml = parse_yaml_header(filepath)
        id_ = None
        if "ID" in yml:
            if isinstance(yml["ID"], list):
                id_ = yml["ID"][0]
            else:
                id_ = str(yml["ID"])
        title = get_title_from_file(filepath)
        if (id_ and id_ in bestehende_eintraege) or os.path.splitext(mdfile)[0] in bestehende_eintraege:
            continue
        if id_:
            link = f"[[{id_}]] {title}\n"
            key = title[0]
        else:
            link = f"[[{os.path.splitext(mdfile)[0]}]] {title}\n"
            key = title[0]
        neue_eintraege.append((key, link))

    if not neue_eintraege:
        print("Keine neuen Einträge gefunden.")
        return

    neue_eintraege.sort(key=lambda x: (x[0].upper(), x[1].lower()))

    for key, line in neue_eintraege:
        insert_entry(index_lines, find_section_indices(index_lines), key, line)

    with open(index_md_path, "w", encoding="utf-8") as f:
        f.writelines(index_lines)

    print(f"{len(neue_eintraege)} neue Einträge zur Index.md hinzugefügt.")

if __name__ == "__main__":
    main()