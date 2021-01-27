import spotipy

import config


class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
            client_id=config.CLIENT_ID,
            client_secret=config.CLIENT_SECRET,
            redirect_uri=config.REDIRECT_URL,
            scope=config.SPOTIFY_SCOPE
        ))

    def get_user_playlists(self, user_id):
        try:
            return [
                {'name': playlist['name'].replace('radio: ', ''), 'id': playlist['id']}
                for playlist in self.sp.user_playlists(user_id)['items']
                if 'radio: ' in playlist['name']
            ]
        except spotipy.exceptions.SpotifyException:
            return []

    def get_playlist_artist_names(self, playlist):
        artists = []
        playlist = self.sp.playlist_items(playlist)
        for track in playlist['items']:
            for artist in track['track']['artists']:
                artists.append(artist['name'])
        return set(artists)

    def name_to_spotify_id(self, name):
        artist = self.sp.search(name, type='artist')['artists']['items'][0]
        return artist['id'], artist['name']

    def artist_to_tracks(self, artist):
        return [track['id']
                for track in self.sp.artist_top_tracks(artist)['tracks']
                if track['is_playable']]

    def track_to_artist_name(self, track_id):
        return self.sp.track(track_id)['artists'][0]['name']
