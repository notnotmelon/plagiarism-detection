import re
from unidecode import unidecode

STOPWORDS = set(['the', 'a', 'an', 'and', 'or', 'of', 'to', 'is', 'are', 'in', 'that', 'it', 'this', 'for', 'on', 'with', 'as', 'be', 'was', 'by', 'if', 'has', 'have', 'had', 'at', 'from', 'but', 'not', 'about', 'so', 'than', 'then', 'too', 'very', 'can', 'could', 'would', 'should', 'will', 'shall', 'may', 'might', 'must', 'do', 'does', 'did', 'done', 'doing', 'dont', 'doesnt', 'didnt', 'doing', 'im', 'ive', 'youre', 'youve', 'theyre', 'theyve', 'weve', 'werent', 'arent', 'isnt', 'wasnt', 'wont', 'cant', 'couldnt', 'wouldnt', 'shouldnt', 'mustnt', 'havent', 'hasnt', 'hadnt', 'thats', 'whats', 'whos', 'wheres', 'whens', 'whys', 'hows', 'whats', 'whos', 'wheres', 'whens', 'whys', 'hows', 'whom', 'who', 'where', 'when', 'why', 'how', 'what', 'which', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever',
'whoever', 'whomever', 'whose', 'whom', 'who', 'where', 'when', 'why', 'how', 'what', 'which', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever', 'whoever', 'whomever', 'whose', 'whomever', 'whichever'])

def preprocessing(text):
    text = text.lower()
    # remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # remove numbers
    text = re.sub(r'\d+', '', text)
    # remove common words
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    # remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # no accents
    text = unidecode(text)
    return text