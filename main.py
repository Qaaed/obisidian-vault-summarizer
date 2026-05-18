import os
import tkinter as tk
from tkinter import filedialog, messagebox

from scanner import scan_vault
from analyzer import analyze_vault


def select_vault_folder():
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(
        title="Select your Obsidian vault folder"
    )

    return folder_path


def print_section(title):
    print("\n" + title)
    print("-" * len(title))


def print_report(analysis):
    print("\n" + "=" * 60)
    print("OBSIDIAN VAULT SUMMARY")
    print("=" * 60)

    print_section("Overview")
    print(f"Total notes: {analysis['total_notes']}")
    print(f"Total words: {analysis['total_words']}")
    print(f"Total internal links: {analysis['total_links']}")

    print_section("Vault Explanation")
    print(analysis["vault_explanation"])

    print_section("Most Common Topics")
    if not analysis["top_topics"]:
        print("No topics found.")
    else:
        for word, count in analysis["top_topics"]:
            print(f"- {word}: {count}")

    print_section("Largest Notes")
    if not analysis["largest_notes"]:
        print("No notes found.")
    else:
        for item in analysis["largest_notes"]:
            print(f"- {item['note']} ({item['word_count']} words)")

    print_section("Most Linked Notes")
    if not analysis["most_linked_notes"]:
        print("No linked notes found.")
    else:
        for item in analysis["most_linked_notes"]:
            print(f"- {item['note']} ({item['backlink_count']} backlinks)")

    print_section("Tiny Notes")
    if not analysis["tiny_notes"]:
        print("No tiny notes found.")
    else:
        for item in analysis["tiny_notes"]:
            print(f"- {item['note']} ({item['word_count']} words)")


def main():
    vault_path = select_vault_folder()

    if not vault_path:
        messagebox.showwarning("No folder selected", "No vault folder was selected.")
        return

    if not os.path.exists(vault_path):
        messagebox.showerror("Error", "The selected vault path does not exist.")
        return

    try:
        print("Scanning vault...")
        notes = scan_vault(vault_path)

        print("Analyzing vault...")
        analysis = analyze_vault(notes)

        print_report(analysis)

        messagebox.showinfo(
            "Scan Complete",
            "Vault summary printed in the terminal."
        )

    except Exception as error:
        messagebox.showerror("Error", f"Something went wrong:\n\n{error}")


if __name__ == "__main__":
    main()