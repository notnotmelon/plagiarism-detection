import stopwords

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

def search(text):
    text = tokenize(stopwords.preprocessing(text))
    results = []
    for tokens in text:
        query = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={tokens}'
        results.append(query)
    print(results[0])
    print(results[1])
    print(results[2])