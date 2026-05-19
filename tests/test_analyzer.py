from analyzer import analyze_vault, build_backlinks, get_tiny_notes, get_top_topics


def sample_notes():
    return {
        "Start": {
            "cleaned_text": "project planning project roadmap ideas",
            "links": ["Roadmap", "Ideas"],
            "word_count": 5,
        },
        "Roadmap": {
            "cleaned_text": "roadmap milestones project",
            "links": ["Ideas"],
            "word_count": 3,
        },
        "Ideas": {
            "cleaned_text": "tiny",
            "links": [],
            "word_count": 1,
        },
    }


def test_get_top_topics_counts_non_stop_words():
    assert get_top_topics(sample_notes(), limit=2) == [("project", 3), ("roadmap", 2)]


def test_build_backlinks_maps_notes_linking_to_each_note():
    backlinks = build_backlinks(sample_notes())

    assert backlinks["Roadmap"] == ["Start"]
    assert backlinks["Ideas"] == ["Start", "Roadmap"]


def test_get_tiny_notes_uses_word_limit():
    tiny_notes = get_tiny_notes(sample_notes(), maximum_words=2)

    assert tiny_notes == [{"note": "Ideas", "word_count": 1}]


def test_analyze_vault_returns_dashboard_data():
    analysis = analyze_vault(sample_notes())

    assert analysis["total_notes"] == 3
    assert analysis["total_words"] == 9
    assert analysis["total_links"] == 3
    assert analysis["most_linked_notes"][0] == {
        "note": "Ideas",
        "backlink_count": 2,
    }
