from urllib.request import urlopen
from bs4 import BeautifulSoup

import stopwords
import google_search

text = '''
in the Microestadio Malvinas Argentinas in the city of Buenos Aires.
Nicolás Vázquez was presented as host.[1] The nominees were presented on
22 August 2011 for 14 categories. Pro-social Award was presented to the
Foundation of Southern Ideas Marcelo Tinelli and the lifetime achievement
award was given to Cris Morena . The musical performances during the awards 
were telecasts Teen Angels. that carry out the single "Que Llegue tu Voz"
and "Mirame, Mirate" from their album TeenAngels 5. Dulce Maria, Tan Bionica 
and Sueña conmigo of performances during the telecast of the event, and each
sang a medley of some of his latest hits.[2][3] As in previous years, 
voting was conducted online through the official website of the program. 
In addition, the network of Facebook page also can vote through Facebook 
accounts 'fans' first channel. The voting period began on 22 August 2011 
and ended on 19 September 2011. The winners were announced on 19 September
2011 during the ceremony.'''

google_search.search(text)

url = 'https://lua-api.factorio.com/latest/classes/LuaGuiElement.html'
html = urlopen(url).read().decode('utf-8')
website_text = stopwords.preprocessing(BeautifulSoup(html, features='html.parser').get_text())
website_tokens = website_text.split()
plagiarised_text = '''his will add a tabbed-pane and 2 tabs with contents.

local tabbed_pane = game.player.gui.top.add{type="tabbed-pane"} meow raw meow rat cat fat bat sat mat hat pat adadsd ake ake afa afa eee \\ g qd qwd 
local tab1 = tabbed_pane.add{type="tab", caption="Tab 1"}
local tab2 = tabbed_pane.add{type="tab", caption="Tab 2"}'''
plagiarised_text = stopwords.preprocessing(plagiarised_text)
plagiarised_tokens = plagiarised_text.split()

paragraph_length = 80 # distance we check for plagiarism on either side of the word
reorganization_length = 8 # weaker distance used to make sure it can still detect out of order plagiarism
def calculate_plagiarisism_score(i, index):
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

i = 0
while i < len(plagiarised_tokens):
    token = plagiarised_tokens[i]
    highest_score = -1
    for index in find_indexes(token, website_tokens):
        plagiarisism_score = calculate_plagiarisism_score(i + 1, index + 1)
        if plagiarisism_score > highest_score:
            highest_score = plagiarisism_score
    if highest_score > 6:
        plagiarisized_substring = plagiarised_tokens[i:i+highest_score]
        print(' '.join(plagiarisized_substring), sep=' ')
        print('score: ' + str(highest_score))
        del plagiarised_tokens[i:i+highest_score]
        print(plagiarised_tokens)
    i += 1