import requests
from concurrent.futures import ThreadPoolExecutor

# api key for google search api
# plaintext :(   (pls dont abuse)
api_key = 'AIzaSyCNFq-e_lzmgQjrxWxcqbqVLoRtfrp04qE'

# custom search engine id
cx = '53e23a42524bc4913'

max_search_words = 32
def tokenize(text):
    tokens = []
    text = text.split()
    while len(text) > 0:
        tokens.append(' '.join(text[0:max_search_words]))
        del text[0:int(max_search_words*0.75)] # 0.75 allows some overlap between search queries
    return tokens

def search(text, results_count):
    text = tokenize(text)
    queries = []
    for tokens in text:
        query = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={tokens}&fields=items(title,link)'
        print(query)
        print('\n\n')
        queries.append(query)
    results = []
    best_results = {}
    title_link_map = {}
    with requests.Session() as s:
        def find_plagiarism_thread(query):
            try:
                results.append(s.get(query).json())
            except Exception as e:
                print(e)
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(find_plagiarism_thread, queries)
    for result in results:
        if 'items' not in result:
            continue
        for ranking, item in enumerate(result['items']):
            link = item['link']
            if link not in best_results:
                best_results[link] = 0
            # score each link according to frequency of occurence & ranking in google search
            best_results[link] += (1/2)**ranking
            title_link_map[link] = item['title']
    top_urls = sorted(best_results, key=best_results.get, reverse=True)[:results_count]
    return top_urls