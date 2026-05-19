import os
import re
from pathlib import PurePath


OBSIDIAN_LINK_PATTERN = r"\[\[([^\]]+)\]\]"


def get_markdown_files(vault_path):
    markdown_files = []

    for root, dirs, files in os.walk(vault_path):
        if ".obsidian" in dirs:
            dirs.remove(".obsidian")

        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                markdown_files.append(full_path)

    return markdown_files


def get_note_name(file_path):
    file_name = os.path.basename(file_path)
    return os.path.splitext(file_name)[0]


def is_markdown_file(file_path):
    return str(file_path).lower().endswith(".md")


def is_obsidian_internal_file(file_path):
    return ".obsidian" in PurePath(str(file_path)).parts


def build_note_data(note_path, content):
    note_name = get_note_name(note_path)
    links = extract_links(content)
    cleaned = clean_text(content)

    return note_name, {
        "path": str(note_path),
        "content": content,
        "cleaned_text": cleaned,
        "links": links,
        "word_count": len(cleaned.split())
    }


def extract_links(content):
    matches = re.findall(OBSIDIAN_LINK_PATTERN, content)

    cleaned_links = []

    for link in matches:
        if "|" in link:
            link = link.split("|")[0]

        if "#" in link:
            link = link.split("#")[0]

        cleaned_links.append(link.strip())

    return cleaned_links


def clean_text(content):
    # Remove Obsidian links but keep the linked text
    content = re.sub(r"\[\[([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]", r"\1", content)

    # Remove markdown symbols
    content = re.sub(r"[#>*_`~\-]", " ", content)

    # Remove URLs
    content = re.sub(r"http\S+", " ", content)

    # Remove extra spaces
    content = re.sub(r"\s+", " ", content)

    return content.strip()


def scan_vault(vault_path):
    notes = {}

    markdown_files = get_markdown_files(vault_path)

    for file_path in markdown_files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        note_name, note_data = build_note_data(file_path, content)
        notes[note_name] = note_data

    return notes


def scan_uploaded_files(uploaded_files):
    notes = {}

    for uploaded_file in uploaded_files:
        file_path = uploaded_file.name

        if not is_markdown_file(file_path):
            continue

        if is_obsidian_internal_file(file_path):
            continue

        content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        note_name, note_data = build_note_data(file_path, content)
        notes[note_name] = note_data

    return notes
