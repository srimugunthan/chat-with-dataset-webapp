# chat-with-dataset-webapp


# Chat with Your Dataset

A Streamlit web app that lets you upload a CSV dataset and ask questions about it using natural language. Powered by LangChain's Pandas DataFrame Agent and OpenAI.

## Prerequisites

- Python 3.11+
- OpenAI API key

## Installation

1. Clone the repository and navigate to the project directory:

```bash
cd chat-with-dataset-webapp
```

2. Create a virtual environment using uv:

```bash
pip install uv
uv venv
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
uv pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Usage

1. Enter your OpenAI API key in the sidebar
2. Upload a CSV file using the file uploader
3. Ask questions about your data in the chat input

### Example Questions

- "How many rows are there?"
- "What are the column names?"
- "What is the average of [column]?"
- "Show me rows where [column] > 100"
- "Plot [column1] vs [column2]"
- "What is the correlation between [column1] and [column2]?"

## Project Structure

```
chat-with-dataset-app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
