import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from llm_summarizer.utils.main import load_files_in_folder, read_file, read_json_file

# Load environment variables and configure Gemini API
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("Key not found")
genai.configure(api_key=API_KEY)

# Directories for stories and tables
STORY_DIR = "llm_summarizer/stories"
TABLE_DIR = "llm_summarizer/tables"
os.makedirs(STORY_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)

def get_latest_story_with_context():
    """
    Returns the latest uploaded story and up to 3 older stories for context.
    If no stories exist, returns an error dict.
    """
    story_files = load_files_in_folder(STORY_DIR)
    if not story_files:
        return {"error": "No stories uploaded yet"}
    # Latest story
    latest_story = read_file(story_files[0])
    older_stories = [read_file(f) for f in story_files[1:4]]
    return latest_story, older_stories

def get_table_metadata():
    """
    Loads metadata for all tables in the tables directory.
    Returns a list of table dicts.
    """
    table_files = load_files_in_folder(TABLE_DIR)
    return [read_json_file(f) for f in table_files]

def run_llm(latest_story, older_stories, tables):
    """
    Runs Gemini LLM to summarize the latest story and match relevant tables.
    Returns the LLM output as a string.
    """
    # Format latest story as readable text
    def format_story(story):
        """Format a story dict as readable text for the prompt."""
        if isinstance(story, dict):
            return f"title: {story.get('title', '')}\ndescription: {story.get('description', '')}"
        return str(story)

    formatted_story = format_story(latest_story)
    # Limit context to 2 older stories
    formatted_context = "\n\n".join([format_story(s) for s in older_stories[:2]]) if older_stories else "No older stories."

    # Reduce table data: only include first 3 table names and descriptions
    reduced_tables = [
        {
            "table_name": t.get("table_name"),
            "description": t.get("description")
        } for t in tables[:3]
    ]

    # Build prompt in sample_llm_input.py format
    tables_str = "\n".join([f"{tbl['table_name']}: {tbl['description']}" for tbl in reduced_tables])
    prompt = f"""
    Summarize the following insurance story and suggest relevant tables. Don't add reference story in
    the output, just show recent uploaded story's summary.

    Story:
    {formatted_story}

    Context:
    {formatted_context}

    Tables:
    {tables_str}

    Format:
    Summary: <short summary and crisp explanation>
    Tables: <comma-separated table names>
    """

    #print("\n--- Gemini Prompt ---\n")
    #print(prompt)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 800
        }
    )
    print("\n--- Gemini Raw Response ---\n")
    print(response)
    try:
        return response.text
    except Exception as e:
        return f"No valid response from LLM. Error: {e}\nRaw response: {response}"

