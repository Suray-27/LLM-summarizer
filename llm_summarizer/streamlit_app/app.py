import streamlit as st
import os
from llm_summarizer.utils.main import save_uploaded_file
from llm_summarizer.summarizer.llm import get_latest_story_with_context,get_table_metadata, run_llm


st.set_page_config(page_title = "AI assistant")
st.title("LLM")

tab1, tab2 = st.tabs(["Upload story", "Run Analysis"])

with tab1:
    st.subheader("Upload a new story")
    uploaded_story = st.file_uploader("Choose a file", type=["json"])
    if uploaded_story and st.button("Enter"):
        save_uploaded_file(uploaded_story, "llm_summarizer/stories")
        st.success(f"Story '{uploaded_story.name}' uploaded!")

with tab2:
    st.subheader("Run LLM Analysis")
    result = get_latest_story_with_context()
    if isinstance(result, dict) and "error" in result:
        st.warning(result["error"])
    else:
        latest_story, older_stories = result
        tables = get_table_metadata()
        if st.button("Run LLM"):
            st.info("Running LLM...Please wait")
            result = run_llm(latest_story, older_stories, tables)
            st.subheader("LLM Result")
            st.write(result)

