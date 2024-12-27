
# Flask Backend for News Summarizer

This is the backend of the News Summarizer Chrome Extension, built using Flask. The backend serves a REST API to process and summarize news content from URLs.

## Features
- Fetches and processes HTML or JSON from the given URL.
- Generates summaries using NLP techniques.
- Removes irrelevant content, such as hashtags, for concise summaries.
- Prioritizes sentences relevant to the news title.

## Requirements

Before you begin, ensure you have the following installed on your machine:
- Python 3.8 or above
- pip (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (if needed):

   Create a `.env` file in the project root and add variables like `FLASK_APP` and `FLASK_ENV`.

## Running the Application

1. Start the Flask development server:

   ```bash
   flask run
   ```

2. The server will be available at `http://127.0.0.1:5000`.

## API Endpoints

### `POST /summarize`
Summarizes the content of a given URL.

#### Request Body:
```json
{
  "url": "https://example.com/news-article"
}
```

#### Response:
```json
{
  "summary": {
         "summary:"Summarized content here..."
   }
}
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
