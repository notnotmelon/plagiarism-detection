import google_search
import plagiarism_checker

text = '''
It might seem crazy what I am 'bout to say
Sunshine, she's here, you can take a break
I'm a hot air balloon that could go to space
With the air, like I don't care, baby by the way
Huh (Because I'm happy)
Clap along if you feel like a room without a roof
(Because I'm happy)
Clap along if you feel like happiness is the truth
(Because I'm happy)
Clap along if you know what happiness is to you
(Because I'm happy)
Clap along if you feel like that's what you wanna do
Here come bad news talking this and that (Yeah)
Well give me all you got, don't hold back (Yeah)
Well I should probably warn you I'll be just fine (Yeah)
No offense to you don't waste your time
Here's why'''

top_urls = google_search.search(text, 10)
if len(top_urls) == 0:
    print('No results found')
else:
    plagiarisized_substrings, unsearchable_urls = plagiarism_checker.find_plagiarism(text, top_urls)
    for substring, url in plagiarisized_substrings:
        print(f'"{substring}" was plagiarized from {url}')
    for url in unsearchable_urls:
        print('Could not search ' + url)