# Spotify Radio
Multiple personalized radio stations on Spotify

## Idea
Music streaming services provide personalized radio stations based on user preferences and music 
genre/style/mood/epoch. However, there is no way to define desired style/mood by yourself.
Here I implemented backend (and redimentary client for a demo purposes) for alternative Spotify client with multiple 
personalized radio stations defined and managed by user.

[Interactive docs](http://95.216.143.9:8080/docs)

## Implementation
The main parts of the service are:
- FastAPI based **webserver**
- **radio station manager**, which handles all business logic (user feedback processing, 
  recommendations postprocessing, track to artist conversion, etc.)
- **vectorizer** implements all logic with item vectorization, searching for items according to listening history 
  and station style
- **Spotify client** is responsible for (obviously) interfacing with Spotify API and could be replaced to provide 
  the same functionality for different music streaming services
  
## Operation details
- service is completely stateless, despite cache for requests to Spotify API (so some warm-up is necessary 
  for new replicas)
- recommender is realtime, which means user feedback (listening history in this case) affects recommendations 
  immediately
- service is model agnostic, ANN index implements abstraction above algorithms (e.g. ALS, BPR, word2vec, lightFM and 
  content-based) which could be swapped with no effort (if similar items have similar vectors and vector arithmetics works) 
- radio could be shared, so you can curate radio station for your followers or make station for particular event
- importance of station style, positive and negative feedback could be adjusted easily and independent of each other

## Model details
- model recommends artists instead of tracks and tracks are sampled by heuristic due to dataset sparsity 
  and a long tail problem distinctive to the music industry
- model trained on the [dataset](https://www.kaggle.com/usasha/million-music-playlists) with a user made playlists 
  scrapped from social network
- dataset was cleaned up massively because artist names are entered by users
- you can find ANNOY index with item vectors and pickle with ID to name mappings in ./data

## How to run it
- open ./notebooks/demo.ipynb in jupyter, here you will find a demo based on rudimentary client
- to make new radio station, create playlist prefixed with 'radio: ' on Spotify; playlist artists will
  define radio station style

## How to modify it
- create Spotify app account as described [here](https://developer.spotify.com/documentation/general/guides/app-settings/)
- build a docker image with your Spotify settings from the root of this repo
```
  docker build
  --build-arg spotify_client_id=<SPOTIFY_CLIENT_ID>
  --build-arg spotify_client_secret=<SPOTIFY_CLIENT_SECRET> 
  -t spotify_radio .
```
- run service `docker run -p 8080:8080 spotify_radio` localy 
- instantiate RadioClient without radio_host parameter