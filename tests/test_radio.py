import pytest

from radio import Radio
from vectorizer import Vectorizer


@pytest.fixture
def radio():
    return Radio()


def test_radio_init(radio):
    assert isinstance(radio.vectorizer, Vectorizer)
    assert radio.spoty is not None


@pytest.mark.parametrize('user_id', [
    'wotetsaz6dvmgp02mv8fcwfvo',
    'no_such_user',
])
def test_radio_available_stations(radio, user_id):
    stations = radio.available_stations(user_id)
    assert isinstance(stations, list)
    for station in stations:
        assert isinstance(station['name'], str)
        assert isinstance(station['id'], str)


@pytest.mark.parametrize('listening_history, n', [
    ([{'track_id': '2IUw7zZ0tyOBePnWKOA1hM',
       'play_seconds': 0,
       'length_seconds': 100},
      {'track_id': '0oRhyzPYXQojkIoSgwmrZy',
       'play_seconds': 100,
       'length_seconds': 100},
      {'track_id': '4f2Lc9C1dhkTMQgA6qIEJd',
       'play_seconds': 100,
       'length_seconds': 100}], 10),
    ({}, 5),
])
def test_radio_next(radio, stations, listening_history, n):
    recommended = radio.next(stations[0], listening_history, n)
    assert recommended != radio.next(stations[1], listening_history, n)

    if listening_history:
        assert recommended != radio.next(stations[0], [], n)

    assert len(recommended) == n
    assert all([isinstance(item, str) for item in recommended])

    seen = {track['track_id'] for track in listening_history}
    assert all([item not in seen for item in recommended])
