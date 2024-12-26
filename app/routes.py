from flask import Blueprint, request, jsonify
from .utils import fetch_and_summarize

main = Blueprint('main', __name__)

@main.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        # Call the utility function for summarization
        summary = fetch_and_summarize(url)
        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500