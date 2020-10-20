import spotify
import asyncio

async def spot_search(search):
    client = spotify.Client('7c53c48485d5470badc45ef1fefb92aa', 'c74a53cbe9d44073a6febdf4cf069cdd')

    results = await client.search(search)

    playlists = results['playlists']

    pl_tracks = {}
    for playlist in playlists[:20]:
        pl_tracks[playlist.name] = []
        tracks = await playlist.get_all_tracks()
        for track in tracks[:50]:
            pl_tracks[playlist.name].append({"artist": track.artist.name, "song": track.name})

    return pl_tracks
# end def spot_search
