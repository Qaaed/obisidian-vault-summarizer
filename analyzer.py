from collections import Counter


STOP_WORDS = {
    "the", "and", "is", "to", "of", "a", "in", "for", "on", "with", "as", "this",
    "that", "it", "be", "are", "was", "were", "or", "an", "by", "from", "at",
    "you", "your", "i", "we", "they", "he", "she", "them", "his", "her", "its",
    "can", "will", "would", "should", "could", "do", "does", "did", "not",
    "if", "then", "else", "when", "what", "how", "why", "which", "who",
    "into", "about", "also", "use", "used", "using", "one", "two", "each",
    "all", "so", "but", "because", "there", "their", "these", "those",
    "has", "have", "had", "my", "me", "our", "us"
}


def get_all_words(notes):
    words = []

    for note_data in notes.values():
        text = note_data["cleaned_text"].lower()
        raw_words = text.split()

        for word in raw_words:
            word = word.strip(".,!?()[]{}:;\"'")

            if len(word) < 3:
                continue

            if word in STOP_WORDS:
                continue

            if word.isnumeric():
                continue

            words.append(word)

    return words


def get_top_topics(notes, limit=15):
    words = get_all_words(notes)
    word_counts = Counter(words)

    return word_counts.most_common(limit)


def get_largest_notes(notes, limit=10):
    sorted_notes = sorted(
        notes.items(),
        key=lambda item: item[1]["word_count"],
        reverse=True
    )

    return [
        {
            "note": note_name,
            "word_count": note_data["word_count"]
        }
        for note_name, note_data in sorted_notes[:limit]
    ]


def get_tiny_notes(notes, maximum_words=20):
    tiny_notes = []

    for note_name, note_data in notes.items():
        if note_data["word_count"] <= maximum_words:
            tiny_notes.append({
                "note": note_name,
                "word_count": note_data["word_count"]
            })

    return tiny_notes


def build_backlinks(notes):
    backlinks = {note_name: [] for note_name in notes}

    for note_name, note_data in notes.items():
        for link in note_data["links"]:
            if link in backlinks:
                backlinks[link].append(note_name)

    return backlinks


def get_most_linked_notes(notes, limit=10):
    backlinks = build_backlinks(notes)

    sorted_backlinks = sorted(
        backlinks.items(),
        key=lambda item: len(item[1]),
        reverse=True
    )

    return [
        {
            "note": note_name,
            "backlink_count": len(linked_from)
        }
        for note_name, linked_from in sorted_backlinks[:limit]
        if len(linked_from) > 0
    ]


def generate_vault_explanation(top_topics):
    topic_names = [topic[0] for topic in top_topics[:5]]

    if not topic_names:
        return "This vault does not contain enough text to generate a meaningful summary."

    topics_text = ", ".join(topic_names)

    return (
        "This vault appears to focus mainly on "
        f"{topics_text}. The most repeated terms suggest these are the main areas "
        "covered across your notes."
    )


def analyze_vault(notes):
    top_topics = get_top_topics(notes)

    total_words = sum(note["word_count"] for note in notes.values())
    total_links = sum(len(note["links"]) for note in notes.values())

    return {
        "total_notes": len(notes),
        "total_words": total_words,
        "total_links": total_links,
        "top_topics": top_topics,
        "largest_notes": get_largest_notes(notes),
        "tiny_notes": get_tiny_notes(notes),
        "most_linked_notes": get_most_linked_notes(notes),
        "vault_explanation": generate_vault_explanation(top_topics)
    }