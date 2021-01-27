import pytest

import config
from spotify_client import SpotifyClient


@pytest.fixture
def client():
    return SpotifyClient(config.SPOTIFY_SETTINGS)


@pytest.mark.parametrize('user_id', [
    'wotetsaz6dvmgp02mv8fcwfvo',
    'no_such_user',
])
def test_client_get_user_playlists(client, user_id):
    playlists = client.get_user_playlists(user_id)
    assert isinstance(playlists, list)
    assert all(isinstance(playlist, dict) for playlist in playlists)

    if playlists:
        assert all('name' in playlist for playlist in playlists)
        assert all('id' in playlist for playlist in playlists)


def test_client_get_playlist_artist_names(client, stations):
    for station in stations:
        artists = client.get_playlist_artist_names(station)
        assert isinstance(artists, set)
        assert all(isinstance(artist, str) for artist in artists)


@pytest.mark.parametrize('name', [
    'no_such_artist',
    'nirvana',
    'the nirvana',
    'кровосток',
])
def test_client_name_to_spotify_id(client, name):
    artist_id, spotify_name = client.name_to_spotify_id(name)
    assert isinstance(artist_id, str)
    assert isinstance(spotify_name, str)


@pytest.mark.parametrize('artist', [
    '6olE6TJLqED3rqDCT0FyPh',
    '211p9eSLzwF6iuXzzP5xTl',
    '0ksNNF08VvPbHDXN06mrYa',
])
def test_atrist_to_tracks(client, artist):
    tracks = client.artist_to_tracks(artist)
    assert isinstance(tracks, list)
    assert all(isinstance(track, str) for track in tracks)
