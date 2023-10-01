import stopwords
from urllib.request import urlopen
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

paragraph_length = 80 # distance we check for plagiarism on either side of the word
reorganization_length = 8 # weaker distance used to make sure it can still detect out of order plagiarism
def calculate_plagiarisism_score(i, index, website_tokens, plagiarised_tokens):
    overestimation = 0
    website_tokens_length = len(website_tokens)
    plagiarised_tokens_length = len(plagiarised_tokens)
    plagiarisism_score = 1
    while i < plagiarised_tokens_length:
        does_token_exist_within_website = plagiarised_tokens[i] in website_tokens[max(0, index-paragraph_length):min(website_tokens_length, index+paragraph_length)]
        if not does_token_exist_within_website:
            does_website_token_exist_within_plagiarised_text = website_tokens[index] in plagiarised_tokens[max(0, i-reorganization_length):min(plagiarised_tokens_length, i+reorganization_length)]
            if does_website_token_exist_within_plagiarised_text:
                overestimation += 1
            else:
                break
        plagiarisism_score += 1
        i += 1
        index += 1
    return plagiarisism_score - overestimation

def find_indexes(element, list):
    return [i for i, x in enumerate(list) if x == element]

busy = False

def is_busy():
    return busy

plagiarised_substrings = []
unsearchable_urls = []
percent = [0]

def results():
    return plagiarised_substrings, unsearchable_urls, percent[0]

def find_plagiarism(plagiarised_text, urls, event):
    plagiarised_text = stopwords.preprocessing(plagiarised_text)
    plagiarised_tokens = plagiarised_text.split()
    original_size = len(plagiarised_tokens)
    plagiarised_substrings.clear()
    unsearchable_urls.clear()
    def find_plagiarism_thread(url):
        try:
            html = BeautifulSoup(urlopen(url).read().decode('utf-8'), features = 'html.parser')
            website_text = stopwords.preprocessing(html.get_text())
            website_tokens = website_text.split()

            i = 0
            while i < len(plagiarised_tokens):
                token = plagiarised_tokens[i]
                highest_score = -1
                for index in find_indexes(token, website_tokens):
                    plagiarisism_score = calculate_plagiarisism_score(i + 1, index + 1, website_tokens, plagiarised_tokens)
                    if plagiarisism_score > highest_score:
                        highest_score = plagiarisism_score
                if highest_score > 13:
                    plagiarised_substring = ' '.join(plagiarised_tokens[i:i+highest_score])
                    plagiarised_substrings.append((plagiarised_substring, url))
                    del plagiarised_tokens[i:i+highest_score]
                    i+=highest_score
                i += 1
        except Exception as e:
            unsearchable_urls.append(url)
    busy = True
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(find_plagiarism_thread, urls)
    busy = False
    percent[0] = len(plagiarised_substrings) / original_size
    if event is not None:
        event.set()
    return plagiarised_substrings, unsearchable_urls, percent[0]