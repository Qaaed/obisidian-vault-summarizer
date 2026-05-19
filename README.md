# Obsidian Vault Summarizer

A local Streamlit dashboard that scans an Obsidian vault and generates a summary
with charts for topics, large notes, linked notes, and tiny cleanup candidates.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
streamlit run app.py
```

Select your Obsidian vault folder in the sidebar and click **Analyze Vault**.

## Test

```powershell
pytest
```
