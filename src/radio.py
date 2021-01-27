import random

from src import config
from src.spotify_client import SpotifyClient
from vectorizer import Vectorizer


class Radio:
    def __init__(self):
        self.spoty = SpotifyClient()
        self.vectorizer = Vectorizer()

    def available_stations(self, user_id):
        return self.spoty.get_user_playlists(user_id)

    def next(self, radio_id, listening_history=None, n=10):
        seed = self.spoty.get_playlist_artist_names(radio_id)

        likes = []
        dislikes = []
        for track in listening_history or []:
            track = dict(track)  # TODO: remove this
            artist = self.spoty.track_to_artist_name(track['track_id'])
            if track['play_seconds'] / track['length_seconds'] > config.DISLIKE_THRESHOLD:
                likes.append(artist)
            else:
                dislikes.append(artist)

        seen = set(likes + dislikes)
        artist_names = self.vectorizer.recommend(seed, likes, dislikes, n + len(seen))

        tracks = []
        for artist_name in artist_names:
            artist_id, spotify_name = self.spoty.name_to_spotify_id(artist_name)
            if spotify_name in seen:
                continue
            artist_tracks = self.spoty.artist_to_tracks(artist_id)
            tracks.append(random.choice(artist_tracks))

        return tracks[:n]
