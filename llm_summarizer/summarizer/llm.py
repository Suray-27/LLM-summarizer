import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from utils.main import load_files_in_folder, read_file, read_json_file

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Key not found")
genai.configure(api_key=API_KEY)


STORY_DIR = "../llm_summarizer/stories"
TABLE_DIR = "../llm_summarizer/tables"
os.makedirs(STORY_DIR, exist_ok=True)
os.makedirs(TABLE_DIR,exist_ok=True)


def get_latest_story_with_context():
    
    story_files = load_files_in_folder(STORY_DIR)
    if not story_files:
        return {"error": "No stories uploaded yet"}

    # Latest story
    latest_story = read_file(story_files[0])
    older_stories = [read_file(f) for f in story_files[1:4]]
    return latest_story, older_stories
    
def get_table_metadata():
    table_files = load_files_in_folder(TABLE_DIR)
    return [read_json_file(f) for f in table_files]

def run_llm(latest_story, context,tables):
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Build prompt
    prompt = f"""
Summarize the following story based on the provided context from older stories and tables.

Latest Story:
{latest_story}

Context from older stories:
{context if context else "No older stories."}

Use these tables to find exact matches for the latest story (Predict):
{json.dumps(tables, indent=2)}

Summary:

1. Give the summary for the latest story.
2. Provide relevant tables.
"""

    # Call Gemini model
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.5,
            "max_output_tokens": 400
        }
    )

    return response.text



"""from google.cloud import storage, aiplatform
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

# Load environment variables from .env file
load_dotenv()

# Credentials
PROJECT_ID = os.getenv("PROJECT_ID")
TABLE_ID = os.getenv("TABLE_ID")
LOCATION = os.getenv("LOCATION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
API_KEY = os.getenv("API_KEY")


# Validate that all required environment variables are set
if not all([PROJECT_ID, LOCATION, BUCKET_NAME, TABLE_ID, API_KEY]):
    raise ValueError("Missing required environment variables (PROJECT_ID, LOCATION, BUCKET_NAME, INDEX_ID)")


storage_client = storage.Client() # To initialize storage bucket
genai.configure(api_key=API_KEY)

#index = aiplatform.MatchingEngineIndex(index_name=TABLE_ID)
#model = aiplatform.generative_models.GenerativeModel("gemini-1.5-flash-001")


def get_latest_story_with_context():
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = sorted(list(bucket.list_blobs(prefix="story/")), key=lambda a: a.time_created, reverse=True)

    if not blobs:
        return {"error":"No stories Uploaded yet"}
    
    tab_bucket = storage_client.bucket(BUCKET_NAME)
    tab_blobs = sorted(list(tab_bucket.list_blobs(prefix="Table/")))


    latest_blob = blobs[0]
    latest_story = latest_blob.download_as_text()

    # Older stories as context
    older_stories = [blob.download_as_text() for blob in blobs[1:6]]
    context_text = "\n\n---\n\n".join(older_stories)

    # search relevant tables
    # match_response = index.match(queries=[latest_story], num_neighbors=3)

    # relevant_tables = []
    # for res in results:
    #     doc = json.loads(res.document["content"])
    #     relevant_tables.append({
    #         "table_name": doc["table_name"],
    #         "columns": doc["columns"]
    #     })
    # if match_response and match_response[0]:
    #     for neighbor in match_response[0]:
    #         try:
    #             doc = json.loads(neighbor.document["content"])
    #             relevant_tables.append({
    #                 "table_name": doc.get("table_name", "N/A"),
    #                 "columns": doc.get("columns", [])
    #             })
    #         except (json.JSONDecodeError, KeyError):
    #             # Skip neighbors with malformed content
    #             continue

    prompt = f

    # Generate summary using Vertex AI LLM (gemini-2.5-flash)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate(
        prompt,
        temperature=0.5,
        max_output_tokens=400
    )


    # model = aiplatform.TextGenerationModel.from_pretrained("gemini-2.5-flash")
    # response = model.predict(prompt,
    #                         temperature = 0.5,
    #                         max_output_tokens = 400)
    # # Generate summary using Vertex AI LLM
    # response = model.generate_content(
    #     prompt,
    #     generation_config={
    #         "temperature": 0.5,
    #         "max_output_tokens": 400
    #     })

    return {
        "summary": response.text,
        "relevant_tables": response.tables
    }
"""
