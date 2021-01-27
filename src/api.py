import os
from typing import List

import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from radio import Radio
from src import config

app = FastAPI()
api_router = APIRouter()
radio = Radio()


class TrackFeedback(BaseModel):
    track_id: str
    play_seconds: int
    length_seconds: int


class Feedback(BaseModel):
    tracks: List[TrackFeedback]


class TracksOutput(BaseModel):
    tracks: List[str]


@api_router.post('/{station_id}/next',
                 tags=['recommendations'],
                 response_model=TracksOutput,
                 summary='Accepts user’s feedback on a track, if present. '
                         'Returns list of next tracks from selected radio station.',
                 response_description='JSON {“tracks”: list of tracks}'
                 )
def next_track(station_id: str, feedback: Feedback):
    return {'tracks': radio.next(station_id, feedback.tracks)}


@api_router.get('/healthcheck',
                tags=['utils'],
                summary='Dummy URL for healthchecks',
                response_description='OK with status 200',
                )
def healthcheck():
    return 'OK'


class Station(BaseModel):
    name: str
    id: str


class StationsOutput(BaseModel):
    stations: List[Station]


@api_router.get('/stations/{user_id}',
                tags=['recommendations'],
                response_model=StationsOutput,
                summary='Returns list of user radio stations.',
                response_description='JSON {“stations”: list of stations}'
                )
def available_radio_stations(user_id: str):
    return {'stations': radio.available_stations(user_id)}


app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        'api:app',
        host='0.0.0.0', port=int(os.environ.get('PORT', 8080)),
        workers=config.ASGI_WORKERS,
    )
