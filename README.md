# Multi-Agent Research Assistant

Research a topic with a coordinated AI workflow that searches the web, reads a relevant webpage, writes a structured report, and critiques the result. The Streamlit interface is in `streamlit_app.py`.

## Project structure

- `streamlit_app.py` — Streamlit interface for submitting topics and viewing or downloading results.
- `pipeline.py` — runs the research steps and returns their outputs.
- `agents.py` — configures the Gemini model and the search, reader, writer, and critic agents.
- `tools.py` — provides Tavily web search and webpage scraping.

## Requirements

Python 3.10 or newer is recommended. Install the project dependencies:

```bash
pip install streamlit python-dotenv langchain langchain-google-genai langchain-tavily rich beautifulsoup4 requests
```

The application uses a Google Gemini API key for language-model calls and a Tavily API key for web search. Create a `.env` file in the project directory:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep `.env` private; do not commit API keys.

## Start the Streamlit interface

```bash
streamlit run streamlit_app.py
```

Enter a focused research topic and select **Start research**. The results include the generated report, critic feedback, source links, search results, and reader notes. You can download the report as Markdown.

### What you get

- A report with an introduction, at least three key findings, a conclusion, and source URLs.
- Critic feedback with scores, weaknesses, and suggested improvements.
- Search output and reader notes to help you check how the report was assembled.

## Run from the terminal

Run the pipeline directly to enter a topic interactively:

```bash
python pipeline.py
```

## Workflow

1. The search agent gathers recent web results and source URLs using Tavily.
2. The reader agent selects a relevant result and extracts webpage content.
3. The writer creates a report with an introduction, key findings, conclusion, and sources.
4. The critic scores the report and suggests improvements.

## Notes

Search results and reports depend on external services and source availability. Verify important claims against the linked sources.
