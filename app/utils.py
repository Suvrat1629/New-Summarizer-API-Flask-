from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import json

# Download NLTK resources once
nltk.download('punkt')
nltk.download('stopwords')

def fetch_and_summarize(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch the URL: {str(e)}"}

    # Detect response content type
    content_type = response.headers.get('Content-Type', '')
    
    if 'application/json' in content_type:
        try:
            data = response.json()
            text = json.dumps(data)  # Flatten JSON content into a string
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response."}
        title = None  # JSON doesn't usually have a title field
    elif 'text/html' in content_type:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
    else:  # Assume plain text or other formats
        text = response.text
        title = None  # No title available for plain text

    # Remove hashtags and unnecessary content
    text = re.sub(r"#\S+", "", text)  # Remove hashtags
    sentences = sent_tokenize(text)

    # Generate keywords from the title (if available)
    title_keywords = []
    if title:
        title_keywords = [
            word.lower() for word in word_tokenize(title)
            if word.isalnum() and word.lower() not in stopwords.words('english')
        ]

    # Preprocess sentences
    stop_words = set(stopwords.words('english'))
    processed_sentences = [
        ' '.join([word for word in word_tokenize(sentence.lower()) if word.isalnum() and word not in stop_words])
        for sentence in sentences
    ]

    # Compute similarity matrix
    vectorizer = TfidfVectorizer()
    try:
        sentence_vectors = vectorizer.fit_transform(processed_sentences)
    except ValueError:
        return {"error": "Empty or insufficient content to summarize."}

    similarity_matrix = cosine_similarity(sentence_vectors)

    # Rank sentences using TextRank, prioritizing title relevance
    scores = np.sum(similarity_matrix, axis=1)
    ranked_sentences = [
        sentences[i] for i in np.argsort(-scores) if any(keyword in processed_sentences[i] for keyword in title_keywords)
    ]

    # Build the summary with relevant sentences and group them in paragraphs
    summary = ""
    if title:
        summary += f"**{title}**\n\n"  # Title as the first heading
    for sentence in ranked_sentences[:5]:  # Adjust the number of sentences as needed
        summary += f"{sentence}\n"

    return {"summary": summary.strip()}
