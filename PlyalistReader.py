"""Given the song and artist generate 1000 of playlist list with the song and artist within
[ one with song, one with the artist ] and return a list of list of these songs"""

import urllib.request, urllib.parse
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import requests

def playlist_reader(song_name):
    """save the song name and artist name and generate the different instances needed to search for the playlist
    """
    request_error = requests.post('https://api.magicplaylist.co/mp/search?txt=starboy', )






