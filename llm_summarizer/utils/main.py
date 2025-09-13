import os
import json
# Directories for stories and tables
STORY_DIR = "llm_summarizer/stories"
TABLE_DIR = "llm_summarizer/tables"
os.makedirs(STORY_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file, folder):
    """
    Save an uploaded file to the specified folder.
    Returns the file path.
    """
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def load_files_in_folder(folder, max_files=None):
    """
    Load and sort files in a folder by modification time (descending).
    Optionally limit to max_files.
    Returns a list of file paths.
    """
    files = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder)],
        key=os.path.getmtime,
        reverse=True
    )
    if max_files:
        files = files[:max_files]
    return files

def read_file(filepath):
    """
    Read and return JSON data from a file.
    """
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)

def read_json_file(filepath):
    """
    Read and return JSON data from a file (alias for read_file).
    """
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)