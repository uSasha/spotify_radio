import pytest

import numpy as np

from vectorizer import Vectorizer


@pytest.fixture
def vectorizer():
    return Vectorizer()


def test_vectorizer_init(vectorizer):
    assert isinstance(vectorizer.name_to_id, dict)
    assert len(vectorizer.name_to_id) > 0

    assert isinstance(vectorizer.id_to_name, dict)
    assert len(vectorizer.id_to_name) > 0

    assert all([item_id in vectorizer.id_to_name
                for name, item_id in vectorizer.name_to_id.items()])
    assert all([name in vectorizer.name_to_id
                for item_id, name in vectorizer.id_to_name.items()])

    assert vectorizer.ann is not None
    assert vectorizer.ann.get_n_items() == len(vectorizer.id_to_name)


@pytest.mark.parametrize('seed, likes, dislikes, n', [
    ([], [], [], 5),
    (['nirvana', 'no_such_item'], [], [], 5),
    (['nirvana', 'korn'], ['the kills'], ['the kills'], 5),
    (['nirvana', 'korn'], ['the kills'], ['2pac'], 5),
    (['nirvana', 'korn'], ['the kills', 'dead weather'], ['2pac', '67'], 5),
])
def test_vectorizer_recommend(vectorizer, seed, likes, dislikes, n):
    recommended = vectorizer.recommend(seed, likes, dislikes, n)
    assert isinstance(recommended, list)
    assert len(recommended) == n
    assert all([isinstance(item, str) for item in recommended])

    if seed:
        assert recommended != vectorizer.recommend([], likes, dislikes, n)
    if likes:
        assert recommended != vectorizer.recommend(seed, [], dislikes, n)
    if dislikes:
        assert recommended != vectorizer.recommend(seed, likes, [], n)

    assert recommended == vectorizer.recommend(seed, likes, dislikes, n)


@pytest.mark.parametrize('items', [
    [],
    ['no_such_item', 'nirvana'],
    ['no_such_item', 'nirvana', 'nirvana']
])
def test_vectorizer_mean_items_vector(vectorizer, items):
    vec = vectorizer._mean_items_vector(items)
    assert isinstance(vec, np.ndarray)
    assert vec.shape == vectorizer._mean_items_vector(items * 2).shape
    if items:
        assert np.linalg.norm(vec) == pytest.approx(1, 0.01)
    else:
        assert np.linalg.norm(vec) == 0
