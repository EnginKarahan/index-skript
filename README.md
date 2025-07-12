# Zettelkasten Index Updater

This Python script automates the maintenance of an `Index.md` file for your Zettelkasten notes.  
It scans the directory where it is located for Markdown files (`.md`), detects new notes, and adds them as alphabetically sorted internal links under the appropriate letter headings in your index.

---

## Features

- Creates an `Index.md` with YAML header and headings for each letter (`## A` to `## Z`, plus `## Ä`, `## Ö`, `## Ü`) if it doesn't exist.
- Detects note titles (from the first Markdown heading or filename) and IDs (from each note's YAML frontmatter).
- Adds new notes as internal wiki-links (`[[ID]] Title` or `[[Filename]] Title`) in the corresponding section.
- Avoids duplicate entries.
- **Works in the directory where the script is placed and run.** All Markdown notes and the index must be in the same folder as the script.

---

## Requirements

- **Python 3**
- **PyYAML** library

Install PyYAML with:

```bash
pip install pyyaml
```

## Usage

1. **Place the script** (`index-skript.py`) into the folder that contains your Markdown notes.

2. **(Optional but recommended)** Set up a Python virtual environment in this folder:
```bash
python3 -m venv .venv 
source .venv/bin/activate # On Linux/macOS .venv\Scripts\activate # On Windows 
pip install pyyaml
```
3. **Run the script** from the command line in that directory:
```bash
python index-skript.py
```
_(Adjust the filename if you use a different name.)_

## Making the Script Executable

### Linux & macOS

To run the script directly (without `python` in front):

1. **Add a shebang** at the very top of `index-skript.py`:

   ```python
   #!/usr/bin/env python3
   ```

2. **Make the script executable**:

   ```bash
   chmod +x index-skript.py
   ```

3. **Run the script directly**:

   ```bash
   ./index-skript.py
   ```

### Windows

On Windows, you can run the script with:

```cmd
python index-skript.py
```

Alternatively, to make it easier:

* Create a batch file named `run_index.bat` in your folder with the following contents:

  ```bat
  @echo off
  python "%~dp0index-skript.py"
  pause
  ```

* Double-click `run_index.bat` to execute the script.

**Note:** The shebang and executable permissions are not required on Windows.

***

## Notes

* The `Index.md` must be in the same directory as your notes and script. If it doesn't exist, it will be created automatically.

* Each note should have a YAML frontmatter section. Example:

  ```yaml
  ---
  ID: 20240101010101
  title: Example Note
  ...
  ```

* The script uses the first Markdown heading (`# Heading`) as the note title. If missing, the filename is used.

* Entries are stored as internal wiki-links (`[[ID]] Title` or `[[Filename]] Title`).\
  This link format is widely supported by modern Markdown editors, such as Zettlr.\
  These links are clickable, enable navigation, and are correctly exported when using tools such as Pandoc.

***

## Example Output (`Index.md`)

```markdown
---
title: "Index"
author:
  - Example Author
date: 2024-01-01
keywords: 
    - Index
    - Zettelkasten
    - Knowledge Management
ID: 
    - 20240101010101
...

# Index

## A

[[20240101010101]] Example Note

## B

[[basicnote]] Basic Note

## C

...

## Ä

## Ö

## Ü
```
