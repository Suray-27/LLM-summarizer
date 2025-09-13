import streamlit as st
import os

from utils.main import save_uploaded_file
from summarizer.llm import get_latest_story_with_context,get_table_metadata, run_llm


st.set_page_config(page_title = "AI assistant")
st.title("LLM")

tab1, tab2 = st.tabs(["Upload story", "Run Analysis"])

with tab1:
    st.subheader("Upload a new story")
    uploaded_story = st.file_uploader("Choose a file", type=["json"])
    if uploaded_story and st.button("Enter"):
        save_uploaded_file(uploaded_story, r"C:\Users\s.bharathi\Downloads\insurance-llm\insurance-llm\story")
        st.success(f"Story '{uploaded_story.name}' uploaded!")

with tab2:
    st.subheader("Run LLM Analysis")
    latest_story, older_stories = get_latest_story_with_context()
    if not latest_story:
        st.warning("No stories available")
    else:
        context = "\n---\n".join([story['text'] for story in older_stories if "text" in story])
        tables = get_table_metadata()
        if st.button("Run LLM"):
            st.info("Running LLM...Please wait")
            result = run_llm(latest_story,context,tables)
            st.subheader("LLM Result")
            st.write(result)

