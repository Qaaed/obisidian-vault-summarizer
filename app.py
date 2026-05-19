import pandas as pd
import streamlit as st

from analyzer import analyze_vault
from scanner import scan_uploaded_files


st.set_page_config(
    page_title="Obsidian Vault Summarizer",
    page_icon="OV",
    layout="wide",
)


def to_dataframe(rows):
    return pd.DataFrame(rows)


def topic_dataframe(top_topics):
    return pd.DataFrame(
        [{"topic": topic, "count": count} for topic, count in top_topics]
    )


def analyze_uploaded_files(uploaded_files):
    notes = scan_uploaded_files(uploaded_files)
    analysis = analyze_vault(notes)
    return notes, analysis


st.title("Obsidian Vault Summarizer")
st.caption("A local dashboard for understanding your notes, links, and cleanup areas.")

with st.sidebar:
    st.header("Vault")
    uploaded_files = st.file_uploader(
        "Select your Obsidian vault folder",
        type=["md"],
        accept_multiple_files="directory",
        help="Choose the vault folder. Only Markdown files are analyzed.",
    )
    analyze_clicked = st.button("Analyze Vault", type="primary")

    st.divider()
    st.caption("This app analyzes the selected Markdown files in your local session.")

if not analyze_clicked:
    st.info("Select your vault folder in the sidebar, then click Analyze Vault.")
    st.stop()

if not uploaded_files:
    st.error("Select a vault folder first.")
    st.stop()

try:
    with st.spinner("Scanning and analyzing vault..."):
        notes, analysis = analyze_uploaded_files(uploaded_files)
except Exception as error:
    st.error(f"Something went wrong while analyzing the vault: {error}")
    st.stop()

if not notes:
    st.warning("No Markdown notes were found in the selected folder.")
    st.stop()

st.subheader("Overview")
metric_columns = st.columns(3)
metric_columns[0].metric("Total notes", analysis["total_notes"])
metric_columns[1].metric("Total words", analysis["total_words"])
metric_columns[2].metric("Internal links", analysis["total_links"])

st.subheader("Vault Explanation")
st.write(analysis["vault_explanation"])

topics_df = topic_dataframe(analysis["top_topics"])
largest_notes_df = to_dataframe(analysis["largest_notes"])
most_linked_df = to_dataframe(analysis["most_linked_notes"])
tiny_notes_df = to_dataframe(analysis["tiny_notes"])

chart_left, chart_right = st.columns(2)

with chart_left:
    st.subheader("Most Common Topics")
    if topics_df.empty:
        st.info("No common topics found.")
    else:
        st.bar_chart(topics_df, x="topic", y="count")
        st.dataframe(topics_df, hide_index=True, use_container_width=True)

with chart_right:
    st.subheader("Largest Notes")
    if largest_notes_df.empty:
        st.info("No notes found.")
    else:
        st.bar_chart(largest_notes_df, x="note", y="word_count")
        st.dataframe(largest_notes_df, hide_index=True, use_container_width=True)

st.subheader("Most Linked Notes")
if most_linked_df.empty:
    st.info("No linked notes found.")
else:
    st.bar_chart(most_linked_df, x="note", y="backlink_count")
    st.dataframe(most_linked_df, hide_index=True, use_container_width=True)

st.subheader("Tiny Notes")
if tiny_notes_df.empty:
    st.success("No tiny notes found.")
else:
    st.write("Notes with 20 words or fewer. These may be cleanup candidates.")
    st.dataframe(tiny_notes_df, hide_index=True, use_container_width=True)
