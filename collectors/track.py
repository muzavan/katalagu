import spotipy

from pprint import pprint

class SpotifyTrackCollector:
    def __init__(self, client:spotipy.Spotify):
        self.client = client

    def get_tracks_from_playlist_id(self, playlist_id=''):
        '''
            Parameters:
                - playlist_id: spotify uri => spotify:playlist:<playlist_id>

            Return
                - tracks: [{title, artist}]
        '''
        tracks = []

        result = self.client.playlist_items(playlist_id, additional_types=['track'])
        res = map(self._get_title_artist, result['items'])
        tracks.extend(list(res))

        while result['next']:
            result = self.client.next(result)
            res = map(self._get_title_artist, result['items'])
            tracks.extend(list(res))

        # Nice to have
        tracks = sorted(tracks, key=lambda x: (x['artist'], x['title']))
            
        return tracks


    def _get_title_artist(self, item):
        track = item.get('track', {})
        track_name = track.get('name', '')

        first_artist = ''
        track_artists = track.get('artists', [])
        if len(track_artists) > 0:
            first_artist = track_artists[0].get('name', '')

        return {
            'title': track_name,
            'artist': first_artist
        }
