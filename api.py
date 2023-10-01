from flask import Flask, jsonify, request
import plagiarism_checker
import google_search

app = Flask(__name__)

@app.route('/plagiarism', methods=['GET'])
def plagiarism():
    text = request.json['text']
    top_urls = google_search.search(text, 10)
    if len(top_urls) == 0:
        return jsonify({'plagiarisized_substrings': [], 'unsearchable_urls': [], 'youtube_urls': []})
    plagiarisized_substrings, unsearchable_urls, youtube_urls = plagiarism_checker.find_plagiarism(text, top_urls)
    return jsonify({'plagiarisized_substrings': plagiarisized_substrings, 'unsearchable_urls': unsearchable_urls, 'youtube_urls': youtube_urls})

if __name__ == '__main__':
    app.run(debug=True)