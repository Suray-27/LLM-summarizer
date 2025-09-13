import streamlit as st
import os
from llm_summarizer.utils.main import save_uploaded_file
from llm_summarizer.summarizer.llm import get_latest_story_with_context, get_table_metadata, run_llm

# Set up Streamlit page configuration
st.set_page_config(
    page_title="AI Insurance Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=80)
    st.markdown("## Welcome! 👋")
    st.info("Use this app to upload insurance stories and run AI-powered analysis to match relevant tables and summarize insights.")
    st.markdown("---")
    st.write("Made with Streamlit & Gemini LLM")

# Main Title and Description
st.markdown("""
    <h1 style='text-align: center; color: #4F8BF9;'>AI Insurance Story Summarizer</h1>
    <p style='text-align: center; color: #555;'>Upload your insurance story and let our AI assistant analyze and match it to relevant tables for actionable insights.</p>
    <br>
    """, unsafe_allow_html=True)

# Tabs for upload and analysis
tab1, tab2 = st.tabs([
    "📤 Upload Story",
    "🧠 Run Analysis"
])

with tab1:
    st.markdown("""
        <h3 style='color: #4F8BF9;'>Upload a New Story</h3>
        <p style='color: #555;'>Supported format: <b>JSON</b></p>
    """, unsafe_allow_html=True)
    uploaded_story = st.file_uploader("Choose a file", type=["json"])
    # Save uploaded story to stories folder
    if uploaded_story:
        if st.button("Upload Story", use_container_width=True):
            save_uploaded_file(uploaded_story, "llm_summarizer/stories")
            st.success(f"✅ Story '{uploaded_story.name}' uploaded!", icon="✅")

with tab2:
    st.markdown("""
        <h3 style='color: #4F8BF9;'>Run LLM Analysis</h3>
        <p style='color: #555;'>The AI will summarize the latest story and match it to relevant tables.</p>
    """, unsafe_allow_html=True)
    # Get latest story and context
    result = get_latest_story_with_context()
    if isinstance(result, dict) and "error" in result:
        st.warning(result["error"], icon="⚠️")
    else:
        latest_story, older_stories = result
        tables = get_table_metadata()
        # Run LLM analysis when button is clicked
        if st.button("Run LLM Analysis", use_container_width=True):
            with st.spinner("Running LLM... Please wait ⏳"):
                llm_result = run_llm(latest_story, older_stories, tables)
            st.success("LLM Analysis Complete!", icon="🤖")
            with st.expander("See Full LLM Output"):
                st.write(llm_result)

