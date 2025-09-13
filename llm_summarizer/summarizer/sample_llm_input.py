# Import Gemini library and configure API key
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables.")
genai.configure(api_key=API_KEY)
# Sample input for LLM summarizer

stories = [
    {
        "story_id": "INS-101",
        "title": "Customer Policy Analytics",
        "description": "Build a pipeline to aggregate customer policy data for analytics.",
        "dependencies": []
    },
    {
        "story_id": "INS-102",
        "title": "Premium Calculation Enhancement",
        "description": "Update premium calculation logic to include risk score adjustments.",
        "dependencies": ["INS-101"]
    },
    {
        "story_id": "INS-103",
        "title": "Claims Fraud Detection",
        "description": "Implement a fraud detection model to flag suspicious claims.",
        "dependencies": ["INS-101", "INS-102"]
    }
]

tables = [
    {
        "table_name": "AGENTS",
        "description": "Insurance agents responsible for policies"
    },
    {
        "table_name": "POLICY",
        "description": "Policy master table containing policy lifecycle details"
    },
    {
        "table_name": "CLAIMS",
        "description": "Claim details raised by policyholders"
    }
]

prompt = f"""
Summarize the following insurance story and suggest relevant tables.

Story:
title: {stories[2]['title']}
description: {stories[2]['description']}

Context:
title: {stories[0]['title']}
description: {stories[0]['description']}

title: {stories[1]['title']}
description: {stories[1]['description']}

Tables:
AGENTS: Insurance agents responsible for policies
POLICY: Policy master table containing policy lifecycle details
CLAIMS: Claim details raised by policyholders

Format:
Summary: <short summary>
Tables: <comma-separated table names>
"""


print(prompt)

# Call Gemini model and print output
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)
print("\n--- Gemini Output ---\n")
try:
    print(response.text)
except Exception as e:
    print(f"No valid response from LLM. Error: {e}\nRaw response: {response}")
