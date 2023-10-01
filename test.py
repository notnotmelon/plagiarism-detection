import requests

with requests.Session() as s:
    r = s.get('http://localhost:5000/plagiarism', json={'text': 'The quick brown fox jumps over the lazy dog'})
    print(r.json())