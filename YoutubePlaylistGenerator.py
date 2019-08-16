"""Takes a list of song titles and returns a url linking to the generated playlist"""
from SongsToYoutube import song_to_youtube

def generate_playlist(list_of_songs):
    vids = ''
    for song in list_of_songs:
        vid_id = song_to_youtube(song).split('=')[1]
        vids = vids + vid_id + ','
    vids = vids[:-1]
    return "http://www.youtube.com/watch_videos?video_ids=" + vids

list = ['hotline bling drake', 'ransom lil tecca', 'i feel it coming the weeknd']

print(generate_playlist(list))

