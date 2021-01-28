import IPython
import ipywidgets as widgets
import requests


class RadioClient:
    def __init__(self, user_id, radio_host='localhost:8080'):
        self.user_id = user_id
        self.current_station = None
        self.radio_host = radio_host.replace('http://', '')
        self.listening_history = []
        self.current_track = None
        self.miniplayer_template = '<iframe src="https://open.spotify.com/embed/track/{track_id}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'

        self.out = widgets.Output()

    @property
    def available_radios(self):
        result = requests.get(f'http://{self.radio_host}/stations/{self.user_id}')
        return result.json()['stations']

    def set_current_station(self, station):
        self.current_station = station['id']

    def start(self):
        dislike = widgets.Button(description='Dislike')
        like = widgets.Button(description='Like')

        dislike.on_click(self.on_dislike_clicked)
        like.on_click(self.on_like_clicked)

        self.current_track = self.get_next_track()
        self.render_page(self.current_track)
        return widgets.VBox([widgets.HBox([dislike, like]), self.out])

    def render_page(self, track_id):
        with self.out:
            IPython.display.clear_output()
            player = widgets.HTML(self.miniplayer_template.format(track_id=track_id))
            IPython.display.display(player)

    def get_next_track(self):
        result = requests.post(f'http://{self.radio_host}/{self.current_station}/next',
                               json={'tracks': self.listening_history})
        return result.json()['tracks'][0]

    def on_like_clicked(self, _):
        self.listening_history.append({
            "track_id": self.current_track,
            "play_seconds": 100,
            "length_seconds": 100,
        })
        self.current_track = self.get_next_track()
        self.render_page(self.current_track)

    def on_dislike_clicked(self, _):
        self.listening_history.append({
            "track_id": self.current_track,
            "play_seconds": 0,
            "length_seconds": 100,
        })
        self.current_track = self.get_next_track()
        self.render_page(self.current_track)
