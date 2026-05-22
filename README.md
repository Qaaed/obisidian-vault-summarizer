# Obsidian Vault Summarizer

A local Streamlit dashboard that scans an Obsidian vault and generates an overview of its structure — including topic clusters, large notes, heavily linked notes, and small cleanup candidates.

## Overview

Obsidian vaults grow fast and become hard to navigate. This tool scans a vault directory, parses the markdown files and their internal links, and produces a visual summary so you can understand what is actually in your vault — what topics dominate, which notes are over-linked or under-developed, and where cleanup is needed.

---

## Features

- Scans any local Obsidian vault folder
- Visualises topic distribution across notes
- Identifies large notes, heavily linked notes, and orphaned or minimal notes
- Runs entirely locally — no data leaves your machine
- Simple one-click analysis via a Streamlit sidebar

---

## Repository Layout

```
obisidian-vault-summarizer/
├── app.py              # Streamlit app entry point
├── main.py             # Core orchestration logic
├── scanner.py          # Vault directory scanner and markdown parser
├── analyzer.py         # Analysis and chart generation
├── tests/              # Pytest test suite
├── requirements.txt
└── pytest.ini
```

---

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

---

## Usage

1. Open the app in your browser (Streamlit will print the local URL on startup).
2. In the sidebar, select your Obsidian vault folder.
3. Click **Analyze Vault**.
4. Browse the generated charts and summary tables.

---

## Running Tests

```bash
pytest
```

---

## License

MIT — see [LICENSE](LICENSE) for details.
