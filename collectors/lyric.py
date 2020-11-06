import lyricsgenius as lg
from time import sleep

class GeniusLyricCollector:
    def __init__(self, client: lg.Genius, batch=100, relax_ms=100):
        self.client = client
        self.batch = batch
        self.relax_ms = 100

    def get_lyric_from_tracks(self, tracks):
        lyrics = []
        cnt = 0
        for track in tracks:
            title, artist = track.get('title', ''), track.get('artist', '')

            if len(title.strip()) == 0:
                continue

            cnt += 1
            try:
                song = self.client.search_song(title=title, artist=artist)
                
                lyric = {
                    "title": title,
                    "artist": artist,
                    "lyric": song.lyrics,
                }
                lyrics.append(lyric)

                print(f"'{title}' by '{artist}' fetched.")
            except:
                print(f"error when fetching lyrics for '{title}' by '{artist}'")

            if cnt % self.batch:
                # Relaxing
                sleep(float(self.relax_ms)/1000.0)
            

        return lyrics



            
            
