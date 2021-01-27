import pickle

import numpy as np
from annoy import AnnoyIndex

from src import config


class Vectorizer:
    def __init__(self):
        with open(config.META_PATH, 'rb') as f:
            meta = pickle.load(f)

        self.name_to_id = meta['name_to_id']
        self.id_to_name = {iid: name for name, iid in self.name_to_id.items()}
        self.ann = AnnoyIndex(meta['vector_size'], meta['distance'])
        self.ann.load(config.ANN_PATH)

    def recommend(self, seed, likes, dislikes, n=10):
        seed_vec = self._mean_items_vector(seed)
        likes_vec = self._mean_items_vector(likes)
        dislikes_vec = self._mean_items_vector(dislikes)

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

    def _mean_items_vector(self, item_names):
        item_ids = [self.name_to_id[name.lower()]
                    for name in item_names
                    if name.lower() in self.name_to_id]
        if not item_ids:
            return np.zeros_like(self.ann.get_item_vector(0))
        items_vec = np.mean([self.ann.get_item_vector(artist) for artist in item_ids], axis=0)
        return items_vec / np.linalg.norm(items_vec)
