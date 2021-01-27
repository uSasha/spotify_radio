from typing import Dict, List, Set, Tuple

import spotipy


class SpotifyClient:
    """
    Wrapper around Spotify API, could be replaced with any other music streaming service.
    """
    def __init__(self, settings: Dict[str, str]) -> None:
        """
        Initialize Spotify client
        :param settings: dict with client id, secret, scope and redirect URI settings
        """
        self.sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(**settings))

    def get_user_playlists(self, user_id: str) -> List[Dict[str, str]]:
        """
        Get public user playlists with prefix 'radio: '
        :param user_id: Spotify user ID
        :return: list of playlist names (without prefix) and IDs
        """
        try:
            return [
                {'name': playlist['name'].replace('radio: ', ''), 'id': playlist['id']}
                for playlist in self.sp.user_playlists(user_id)['items']
                if 'radio: ' in playlist['name']
            ]
        except spotipy.exceptions.SpotifyException:
            return []

    def get_playlist_artist_names(self, playlist: str) -> Set[str]:
        """
        Get artist names from selected playlist.
        :param playlist: Spotify playlist ID (must be public)
        :return: set of artist names
        """
        artists = []
        playlist = self.sp.playlist_items(playlist)
        for track in playlist['items']:
            for artist in track['track']['artists']:
                artists.append(artist['name'])
        return set(artists)

    def name_to_spotify_id(self, name: str) -> Tuple[str]:
        """
        Convert artist name to Spotify ID,
        method will return ID AND spotify name to be able to check distance between requests and found names.
        :param name: artist name
        :return: artist ID and artist name
        """
        artist = self.sp.search(name, type='artist')['artists']['items'][0]
        return artist['id'], artist['name']

    def artist_to_tracks(self, artist: str) -> List[str]:
        """
        Get top tracks for requested artist.
        :param artist: artist ID
        :return: list of track IDs
        """
        return [track['id']
                for track in self.sp.artist_top_tracks(artist)['tracks']
                if track['is_playable']]

    def track_to_artist_name(self, track_id: str) -> str:
        """
        Convert track ID to artist name
        :param track_id: Spotify track ID
        :return: artist name
        """
        try:
            return self.sp.track(track_id)['artists'][0]['name']
        except spotipy.exceptions.SpotifyException:
            return None
