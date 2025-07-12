# Zettelkasten Index Updater

This Python script automates the maintenance of an `Index.md` file in the Zettelkasten style.  
It scans your directory for Markdown files (`.md`), checks whether they are already listed in the index, and, if necessary, adds new entries **sorted alphabetically** under the correct letter headings.

---

## Features

- Creates a new `Index.md` with YAML header and all section headings (`## A` to `## Z`, as well as `## Ä`, `## Ö`, `## Ü`) if needed.
- Automatically detects the title (first heading or filename) and the ID (from YAML).
- Adds new notes as a wiki link (`[[ID]] Title` or `[[Filename]] Title`) at the appropriate position.
- Prevents duplicate entries.

---

## Requirements

- **Python 3**
- **PyYAML** library

Install PyYAML with:

```bash
pip install pyyaml
