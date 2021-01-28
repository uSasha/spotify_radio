import random
from typing import List, Dict, Union

from src import config
from src.spotify_client import SpotifyClient
from vectorizer import Vectorizer


class Radio:
    """
    Radio which can find available stations and provide next tracks according to listening history.
    """
    def __init__(self) -> None:
        self.spoty = SpotifyClient(config.SPOTIFY_SETTINGS)
        self.vectorizer = Vectorizer()

    def available_stations(self, user_id: str) -> List[Dict[str, str]]:
        """
        Get user radio stations.
        Stations are generated from Spotify playlists with prefix 'radio: '. Playlists should be public.
        :param user_id:
        :return:
        """
        return self.spoty.get_user_playlists(user_id)

    def next(self, radio_id: str, listening_history: List[Dict[str, Union[str, int]]] = None, n: int = 10) -> List[str]:
        """
        Find N items within radio station style and with respect to provided listening history.
        :param radio_id: ID if Spotify playlist which describes station style
        :param listening_history: listening stats for previous tracks
        :param n: number of items to return
        :return: Spotify track IDs
        """
        seed = self.spoty.get_playlist_artist_names(radio_id)

        likes = []
        dislikes = []
        for track in listening_history or []:
            track = dict(track)  # TODO: remove this
            artist = self.spoty.track_to_artist_name(track['track_id'])
            if artist is None:
                continue
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
