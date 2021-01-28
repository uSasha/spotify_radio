import pytest
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == "OK"


@pytest.mark.parametrize('station', ['21jrjoe0YmFdSildIeZEyz', '1qH4QR427LghS8CFKy4sbd'])
@pytest.mark.parametrize('listening_history', [
    {'tracks': []},
    {"tracks": [
        {
            "track_id": "1dvKuEV0o8rPfi15oJIPDU",
            "play_seconds": 100,
            "length_seconds": 120
        },
        {
            "track_id": "7CH00lP1L9jRAD7iQkbrID",
            "play_seconds": 10,
            "length_seconds": 120
        }
    ]},
    {"tracks": [
        {
            "track_id": "no_such_track",
            "play_seconds": 0,
            "length_seconds": 120
        },
        {
            "track_id": "7CH00lP1L9jRAD7iQkbrID",
            "play_seconds": 0,
            "length_seconds": 120
        }
    ]},
    {"tracks": [
        {
            "track_id": "1dvKuEV0o8rPfi15oJIPDU",
            "play_seconds": 0,
            "length_seconds": 120
        },
        {
            "track_id": "7CH00lP1L9jRAD7iQkbrID",
            "play_seconds": 0,
            "length_seconds": 120
        }
    ]},
])
def test_api_next_track(station, listening_history):
    """
    Checks that if no feedback or partial feedback payload is provided,
    the endpoint still returns sampled tracks and no attempt
    to send any feedback is made.
    """
    res = client.post(f'/{station}/next', json=listening_history)

    assert res.status_code == 200
    tracks = res.json()['tracks']
    assert isinstance(tracks, list)
    assert len(tracks)
    assert all(isinstance(track, str) for track in tracks)


@pytest.mark.parametrize('station', ['21jrjoe0YmFdSildIeZEyz', '1qH4QR427LghS8CFKy4sbd'])
@pytest.mark.parametrize('listening_history', [
    {"tracks": [
        {
            "play_seconds": 0,
            "length_seconds": 120
        },
    ]},
    {"tracks": [
        {
            "track_id": "1dvKuEV0o8rPfi15oJIPDU",
            "length_seconds": 120
        },
    ]},
    {"tracks": [
        {
            "track_id": "1dvKuEV0o8rPfi15oJIPDU",
            "play_seconds": 0,
        },
    ]},
])
def test_api_next_broken_feedback(station, listening_history):
    res = client.post(f'/{station}/next', json=listening_history)

    assert res.status_code == 422


@pytest.mark.parametrize('user_id', ['wotetsaz6dvmgp02mv8fcwfvo', 'no_such_user'])
def test_api_user_stations(user_id):
    res = client.get(f'/stations/{user_id}')

    assert res.status_code == 200
    stations = res.json()['stations']
    assert isinstance(stations, list)
    assert all(isinstance(station, dict) for station in stations)

    assert all('name' in station for station in stations)
    assert all('id' in station for station in stations)
