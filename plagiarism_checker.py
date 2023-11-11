import stopwords
from urllib.request import urlopen
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

paragraph_length = 80 # distance we check for plagiarism on either side of the word
reorganization_length = 8 # weaker distance used to make sure it can still detect out of order plagiarism
# Function to calculate plagiarism score
def calculate_plagiarisism_score(i, index, website_tokens, plagiarised_tokens):
    overestimation = 0 # this algorithm tends to generate a "tail" of extra plagiarized words. this variable is used to chop off the tail
    website_tokens_length = len(website_tokens)
    plagiarised_tokens_length = len(plagiarised_tokens)
    plagiarisism_score = 1
    while i < plagiarised_tokens_length:
        # Check if the plagiarised token exists within the website tokens
        # Use a sliding window algorithm. Each index is checked if it exists in the destination 80 words fowards and 80 words backwards
        does_token_exist_within_website = plagiarised_tokens[i] in website_tokens[max(0, index-paragraph_length):min(website_tokens_length, index+paragraph_length)]
        if does_token_exist_within_website:
            overestimation = 0
        else:
            # If the inital check fails, try it in reverse: check if the website token exists within the plagiarised text
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

busy = False # used in multithreading

def is_busy(): # impossible to check a boolean from another file. wrap it in a function
    return busy

plagiarised_substrings = []
unsearchable_urls = []
percent = [0] # used to update the progress bar. it must be a list because it's mutable. percent[1] is never used

def results():
    return plagiarised_substrings, unsearchable_urls, percent[0]

def find_plagiarism(plagiarised_text, urls, event):
    plagiarised_text = stopwords.preprocessing(plagiarised_text)
    plagiarised_tokens = plagiarised_text.split()
    original_size = len(plagiarised_tokens)
    plagiarised_substrings.clear()
    unsearchable_urls.clear()
    def find_plagiarism_thread(url): # this function thread-safe
        try:
            # use bs4 to decode the html. does not work on .pdf sites
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
                        highest_score = plagiarisism_score # calculate the highest score from all websites
                if highest_score > 13: # less than 13 similar words can easily happen from random chance. 14 is a good threshold
                    plagiarised_substring = ' '.join(plagiarised_tokens[i:i+highest_score]) # save the bits of plagiarised text to display in the result
                    plagiarised_substrings.append((plagiarised_substring, url))
                    del plagiarised_tokens[i:i+highest_score] # we have already detected this text as plagarized, no need to keep checking it (this operation is threadsafe)
                    i+=highest_score
                i += 1
        except Exception as e:
            unsearchable_urls.append(url) # for some reason bs4 failed on this url. just append the url to display in the result
    busy = True
    with ThreadPoolExecutor(max_workers=5) as executor: # execute 5 threads at a time until the job is finished
        executor.map(find_plagiarism_thread, urls)
    busy = False
    percent[0] = 1 - len(plagiarised_tokens) / original_size # calc the final % score
    if event is not None:
        event.set()
    return plagiarised_substrings, unsearchable_urls, percent[0] # thankfully we can return multiple values