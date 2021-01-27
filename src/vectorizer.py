import pickle
from typing import Sequence, List

import numpy as np
from annoy import AnnoyIndex

from src import config


class Vectorizer:
    """
    Class which handles item and items lists vectorization, searching for nearest items etc.
    Input and output items are names, all IDs are for internal use only.
    """
    def __init__(self, ann_path: str = None, meta_path: str = None) -> None:
        """
        Loads model and ID to name mappings
        :param ann_path: path to ANNOY index file stored on disk
        :param meta_path: path to pickle with meta information (name to ID mapping, vector size and distance type)
        """
        with open(meta_path or config.META_PATH, 'rb') as f:
            meta = pickle.load(f)

        self.name_to_id = meta['name_to_id']
        self.id_to_name = {iid: name for name, iid in self.name_to_id.items()}
        self.ann = AnnoyIndex(meta['vector_size'], meta['distance'])
        self.ann.load(ann_path or config.ANN_PATH)

    def recommend(self, seed: Sequence[str] = None,
                  likes: Sequence[str] = None,
                  dislikes: Sequence[str] = None, n=10) -> List[str]:
        """
        Find N items similar to provided feed and like and different from dislikes.
        this method is deterministic and will always return same items for same input.
        :param seed: items which describe desired genre, mood and or style
        :param likes: items with positive feedback from user
        :param dislikes: items with negative feedback from user
        :param n: number of items to return
        :return: recommended items
        """
        seed = seed or []
        likes = likes or []
        dislikes = dislikes or []

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

    def _mean_items_vector(self, item_names: Sequence[str]) -> np.ndarray:
        """
        Compute mean vector for given list of items. Final vector will be normalized.
        Unknown items will be omitted.
        :param item_names: list of item names
        :return: normalized vector
        """
        item_ids = [self.name_to_id[name.lower()]
                    for name in item_names
                    if name.lower() in self.name_to_id]
        if not item_ids:
            return np.zeros_like(self.ann.get_item_vector(0))
        items_vec = np.mean([self.ann.get_item_vector(artist) for artist in item_ids], axis=0)
        return items_vec / np.linalg.norm(items_vec)
