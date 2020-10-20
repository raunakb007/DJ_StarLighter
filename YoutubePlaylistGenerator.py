
"""Takes a list of song titles and returns a url linking to the generated playlist"""

from __future__ import unicode_literals
from SongsToYoutube import song_to_youtube
import youtube_dl
import time

def generate_playlist(list_of_songs):
    vids = ''
    for song in list_of_songs:
        vid_id = song_to_youtube(song).split('=')[1]
        vids = vids + vid_id + ','
    vids = vids[:-1]
    return "http://www.youtube.com/watch_videos?video_ids=" + vids

def download_playlist(list_of_songs):
    list_files = []
    for song in list_of_songs:
        vid_id = song_to_youtube(song)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([vid_id])
            list_files.append(ydl)
    return list_files

def download_playlist_wave(list_of_songs):
    list_files = []
    for song in list_of_songs:
        vid_id = song_to_youtube(song)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192'
            }],
            'postprocessor_args': [
                '-ar', '16000'
            ],
            'prefer_ffmpeg': True,
            'keepvideo': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([vid_id])
            list_files.append(ydl)
    return list_files

#def download_entire_playlist():


