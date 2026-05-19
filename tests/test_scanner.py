from io import BytesIO

from scanner import (
    clean_text,
    extract_links,
    get_markdown_files,
    scan_uploaded_files,
    scan_vault,
)


class UploadedFileStub(BytesIO):
    def __init__(self, name, content):
        super().__init__(content.encode("utf-8"))
        self.name = name


def test_extract_links_cleans_aliases_and_headings():
    content = "[[Projects]] [[Books|reading list]] [[Ideas#Next steps]]"

    assert extract_links(content) == ["Projects", "Books", "Ideas"]


def test_clean_text_keeps_link_text_and_removes_markdown():
    content = "# Heading\nRead [[Project Alpha|the plan]] at https://example.com"

    assert clean_text(content) == "Heading Read Project Alpha at"


def test_get_markdown_files_ignores_obsidian_folder(tmp_path):
    (tmp_path / "note.md").write_text("Visible note", encoding="utf-8")
    (tmp_path / ".obsidian").mkdir()
    (tmp_path / ".obsidian" / "hidden.md").write_text("Hidden", encoding="utf-8")

    markdown_files = get_markdown_files(tmp_path)

    assert len(markdown_files) == 1
    assert markdown_files[0].endswith("note.md")


def test_scan_vault_reads_markdown_notes(tmp_path):
    (tmp_path / "Start.md").write_text(
        "# Start\nThis links to [[Target]].",
        encoding="utf-8",
    )

    notes = scan_vault(tmp_path)

    assert notes["Start"]["links"] == ["Target"]
    assert notes["Start"]["word_count"] == 5


def test_scan_uploaded_files_reads_markdown_files():
    uploaded_files = [
        UploadedFileStub("Vault/Start.md", "# Start\nLinks to [[Target]]."),
        UploadedFileStub("Vault/image.png", "not markdown"),
    ]

    notes = scan_uploaded_files(uploaded_files)

    assert list(notes) == ["Start"]
    assert notes["Start"]["links"] == ["Target"]


def test_scan_uploaded_files_ignores_obsidian_folder():
    uploaded_files = [
        UploadedFileStub("Vault/.obsidian/config.md", "Hidden"),
        UploadedFileStub("Vault/Visible.md", "Visible note"),
    ]

    notes = scan_uploaded_files(uploaded_files)

    assert list(notes) == ["Visible"]
