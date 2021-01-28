import os

META_PATH = '../data/meta.pkl'
ANN_PATH = '../data/items.ann'
DISLIKE_THRESHOLD = 0.8

SEED_WEIGHT = 1
LIKES_WEIGHT = 0.6
DISLIKES_WEIGHT = 0.3

ASGI_WORKERS = 1

SPOTIFY_SETTINGS = {
    'client_id': os.environ.get('SPOTIFY_CLIENT_ID'),
    'client_secret': os.environ.get('SPOTIFY_CLIENT_SECRET'),
    'redirect_uri': os.environ.get('SPOTIFY_REDIRECT_URI'),
    'scope': 'user-library-read',
}

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
