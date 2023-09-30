import stopwords
import requests

# api key for google search api
api_key = 'AIzaSyBWd9hccN3Xkt5uDuHBTJWWurC-zMZT1to'

# custom search engine id
cx = '53e23a42524bc4913'

max_search_words = 32
def tokenize(text):
    tokens = []
    text = text.split()
    while len(text) > 0:
        tokens.append(' '.join(text[0:max_search_words]))
        del text[0:int(max_search_words*0.75)]
    return tokens

def search(text, results_count):
    text = tokenize(stopwords.preprocessing(text))
    print(text)
    queries = []
    for tokens in text:
        query = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={tokens}&fields=items(title,link)'
        queries.append(query)
        break # REMOVE THIS
    results = []
    best_results = {}
    title_link_map = {}
    with requests.Session() as s:
        for query in queries:
            r = s.get(query)
            results.append(r.json())
    for result in results:
        for ranking, item in enumerate(result['items']):
            link = item['link']
            if link not in best_results:
                best_results[link] = 0
            # score each link according to frequency of occurence & ranking in google search
            best_results[link] += (1/2)**ranking
            title_link_map[link] = item['title']
    print(best_results)
    top = sorted(best_results, key=best_results.get, reverse=True)[:results_count]
    print(top)