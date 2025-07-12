import os
import re
import yaml
from collections import defaultdict

arbeitsverzeichnis = os.getcwd()
index_md_path = os.path.join(arbeitsverzeichnis, "Index.md")

def get_md_files():
    return sorted([f for f in os.listdir(arbeitsverzeichnis)
                   if f.endswith(".md") and f != "Index.md"])

def parse_yaml_header(filepath):
    """Parse YAML header und gibt ein dict zurück."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()
    if lines[0].strip() != "---":
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
    """Nimmt erste Markdown-Überschrift als Titel, sonst Dateiname."""
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("# ").strip()
    return os.path.splitext(os.path.basename(filepath))[0]

def parse_index_entries(index_lines):
    """Sammelt alle bestehenden IDs und Dateinamen aus der Index.md."""
    eintraege = set()
    link_re = re.compile(r"\[\[([^\]]+)\]\]")
    for line in index_lines:
        for match in link_re.finditer(line):
            eintraege.add(match.group(1))
    return eintraege

def find_section_indices(lines):
    """Findet, an welchen Zeilen die Abschnittsüberschriften (## A, ...) stehen."""
    indices = {}
    for i, line in enumerate(lines):
        m = re.match(r"^## ([A-ZÄÖÜ])\s*$", line)
        if m:
            indices[m.group(1)] = i
    return indices

def insert_entry(lines, section_indices, entry_key, entry_line):
    """Fügt einen Eintrag in die korrekte Sektion ein (alphabetisch sortiert)."""
    key = entry_key.upper()
    if key not in section_indices:
        # Neue Sektion einfügen
        # Finde korrekten Platz
        keys = sorted(list(section_indices.keys()) + [key])
        pos = keys.index(key)
        # Wo einfügen?
        # Nach letzter existierender Sektion oder nach Header
        if pos == 0:
            insert_at = max(section_indices.values()) + 1
        else:
            prev_section = keys[pos - 1]
            # Finde Ende der vorherigen Sektion
            prev_idx = section_indices[prev_section]
            insert_at = prev_idx + 1
            while insert_at < len(lines) and not lines[insert_at].startswith("## "):
                insert_at += 1
        # Füge neue Section-Überschrift und Eintrag ein
        lines.insert(insert_at, f"## {key}\n")
        lines.insert(insert_at + 1, entry_line)
        return

    # Füge alphabetisch in bestehende Sektion ein
    idx = section_indices[key] + 1
    # Finde das Ende der Sektion
    end_idx = idx
    while end_idx < len(lines) and not lines[end_idx].startswith("## "):
        end_idx += 1
    # Finde richtige Position in alphabetischer Reihenfolge
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

def main():
    if not os.path.exists(index_md_path):
        print("Index.md nicht gefunden!")
        return

    # Lade Index.md
    with open(index_md_path, encoding="utf-8") as f:
        index_lines = f.readlines()

    # Bestehende Einträge sammeln (IDs und Dateinamen)
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
        # Prüfe, ob es einen Eintrag mit ID ODER Dateiname gibt
        if (id_ and id_ in bestehende_eintraege) or mdfile in bestehende_eintraege:
            continue  # Bereits eingetragen
        # Entscheide, ob ID oder Dateiname als Link
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

    # Neue Einträge alphabetisch nach Key, dann Titel
    neue_eintraege.sort(key=lambda x: (x[0].upper(), x[1].lower()))

    # Füge neue Einträge in die Index.md ein
    for key, line in neue_eintraege:
        insert_entry(index_lines, section_indices, key, line)
        # Nach jedem Insert müssen die indices neu berechnet werden!
        section_indices = find_section_indices(index_lines)

    # Schreibe zurück
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.writelines(index_lines)

    print(f"{len(neue_eintraege)} neue Einträge zur Index.md hinzugefügt.")

if __name__ == "__main__":
    main()