import pickle
import random

import numpy as np
from annoy import AnnoyIndex

from src import config
from src.spotify_client import SpotifyClient


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


class Vectorizer:
    def __init__(self):
        with open(config.META_PATH, 'rb') as f:
            meta = pickle.load(f)

        self.name_to_id = meta['name_to_id']
        self.id_to_name = {iid: name for name, iid in self.name_to_id.items()}
        self.ann = AnnoyIndex(meta['vector_size'], meta['distance'])
        self.ann.load(config.ANN_PATH)

    def recommend(self, seed, likes, dislikes, n=10):
        seed_vec = self.mean_items_vector(seed)
        likes_vec = self.mean_items_vector(likes)
        dislikes_vec = self.mean_items_vector(dislikes)

        query_vec = (
                seed_vec * config.SEED_WEIGHT
                + likes_vec * config.LIKES_WEIGHT
                - dislikes_vec * config.DISLIKES_WEIGHT
        )

        try:
            artist_ids = self.ann.get_nns_by_vector(query_vec, n+1)[1:]
        except ValueError:
            return []
        return [self.id_to_name.get(artist) for artist in artist_ids]

    def mean_items_vector(self, item_names):
        item_ids = [self.name_to_id[name.lower()]
                    for name in item_names
                    if name.lower() in self.name_to_id]
        if not item_ids:
            return np.zeros_like(self.ann.get_item_vector(0))
        items_vec = np.mean([self.ann.get_item_vector(artist) for artist in item_ids], axis=0)
        return items_vec / np.linalg.norm(items_vec)
