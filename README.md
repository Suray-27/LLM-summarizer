# Genius Gist-o-Matic

A Streamlit-powered application that uses Google Gemini LLM to summarize insurance stories and match them to relevant database tables. Upload your insurance stories in JSON format and get instant AI-driven insights and table recommendations.

## Features

- Upload insurance stories in JSON format
- Summarize the latest story using Gemini LLM
- Match stories to relevant tables
- Visually appealing and user-friendly Streamlit interface
- Easy extensibility for new story and table types

## Getting Started

### Prerequisites

- Python 3.8+
- [Google Gemini API key](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

### Installation

1. Clone the repository:
	```bash
	git clone https://github.com/yourusername/insurance-story-ai-summarizer.git
	cd insurance-story-ai-summarizer
	```

2. Create and activate a virtual environment:
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

3. Install dependencies:
	```bash
	pip install -r requirements.txt
	```

4. Set up your `.env` file with your Gemini API key:
	```
	API_KEY=your_gemini_api_key_here
	```

### Running the App

To start the Streamlit app, run:

```bash
PYTHONPATH=/workspaces/LLM-summarizer .venv/bin/streamlit run llm_summarizer/streamlit_app/app.py
```

Then open the provided local URL in your browser.

## Project Structure

```
llm_summarizer/
	stories/         # Uploaded insurance stories (JSON)
	tables/          # Table metadata (JSON)
	summarizer/      # LLM logic and sample input
	streamlit_app/   # Streamlit UI
	utils/           # Utility functions
README.md
requirements.txt
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
