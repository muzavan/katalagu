import click
import json
import lyricsgenius as lg
from pathlib import Path

import spotipy
import sys

from collectors.track import SpotifyTrackCollector
from collectors.lyric import GeniusLyricCollector


def get_tracks(playlist_id, config):
    SPOTIFY_CLIENT_ID = config.get('spotify', {}).get('client_id', '')
    SPOTIFY_CLIENT_SECRET = config.get('spotify', {}).get('client_secret', '')

    sp_auth = spotipy.SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

    sp_client = spotipy.Spotify(auth_manager=sp_auth)

    track_collector = SpotifyTrackCollector(sp_client)

    return track_collector.get_tracks_from_playlist_id(playlist_id)

def get_lyrics(tracks, config):
    GENIUS_CLIENT_ACCESS_TOKEN = config.get('genius', {}).get('client_access_token', '')
    lg_client = lg.Genius(client_access_token=GENIUS_CLIENT_ACCESS_TOKEN)
    lyric_collector = GeniusLyricCollector(lg_client)

    return lyric_collector.get_lyric_from_tracks(tracks)

@click.command()
@click.option('-u', '--uri', required=True, help='Spotify URI to the playlist. You can find it in Share > Copy Spotify URI. Should be in \'spotify:playlist:...\' format')
@click.option('-c', '--creds-json', required=True, help='Path to credentials json file. The format can be seen in creds.json.sample')
@click.option('-o', '--output-json', help='Path to lyrics json file. If not set, will output to current directory with <playlist_id>.json')
@click.option('-t', '--tracks-only', is_flag=True, default=False, help='Using this flag, katalagu will only fetch the tracks list for the playlist.')
def katalagu(uri, creds_json, output_json, tracks_only):
    if not uri.startswith('spotify:playlist:'):
        click.echo("invalid spotify uri")
        return

    playlist_id = uri.split(':')[-1]

    config = {}
    with open(creds_json, "r") as f:
        config = json.load(f)

    if not output_json or len(output_json) == 0:
        output_json = f"{playlist_id}.json"
    # Make sure it exists first
    with open(output_json, "w") as f:
        pass
    
    tracks = get_tracks(playlist_id, config)
    with open(output_json, 'w') as f:
        json.dump({"tracks": tracks}, f, indent=4, sort_keys=True)

    click.echo("fetch tracks list done!")
    if tracks_only:
        return

    click.echo("fetch all lyrics..")
    lyrics = get_lyrics(tracks, config)
    with open(output_json, "w") as f:
        json.dump({"lyrics": lyrics}, f, indent=4, sort_keys=True)

    click.echo(f"fetch {len(lyrics)} done lyrics from {len(tracks)} expected.")

if __name__ == "__main__":
    katalagu()
