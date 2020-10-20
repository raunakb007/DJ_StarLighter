"""given a list of songs, find both the original song + the acapela version as a dictionary ie
{{original_songs: {name : link}, {name2:link} ...}, {acapela_songs: {name: link}, {name: link}}}"""

import urllib.request, urllib.parse
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


def song_to_youtube(song_name):
    search_results = {}
    textToSearch = song_name
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for i in range(0, 5):
        title = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[i]['title']
        search_results[title] = fuzz.ratio(textToSearch, title)
    best_match = max(search_results, key=search_results.get)
    for i in range(0, 5):
        if soup.findAll(attrs={'class': 'yt-uix-tile-link'})[i]['title'] == best_match:
            return ('https://www.youtube.com' + soup.findAll(attrs={'class': 'yt-uix-tile-link'})[i]['href'])


