import os
import json

STORY_DIR = "llm_summarizer/stories"
TABLE_DIR = "llm_summarizer/tables"

os.makedirs(STORY_DIR, exist_ok=True)
os.makedirs(TABLE_DIR,exist_ok=True)

def save_uploaded_file(uploaded_file, folder):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def load_files_in_folder(folder, max_files = None):
    files = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder)],
        key=os.path.getmtime,
        reverse=True
    )

    if max_files:
        files = files[:max_files]
    return files

def read_file(filepath):
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)
    
def read_json_file(filepath):
    with open(filepath,"r", encoding = 'utf-8') as f:
        return json.load(f)