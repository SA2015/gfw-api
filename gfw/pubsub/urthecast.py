import datetime
import time
import json
import os

import requests
from geomet import wkt

BASEURL = 'https://www.urthecast.com/v1/api/apps/subscriptions'
KEY = os.environ['URTHECAST_KEY']
SECRET = os.environ['URTHECAST_SECRET']

# reference payload from API docs
SAMPLEPAYLOAD = '''{
   "title": "San Francisco",
   "email_notification": 1,
   "urthecast_notification": 1,
   "text_message_notification": 0,
   "start_date": 1410205766,
   "end_date": 1410205766,
   "geometry": "POLYGON ((-122.51129150390625 37.71560291938265,-122.52056121826172 37.789437981475004,-122.49069213867188 37.79323632157157,-122.48210906982423 37.81059767530207,-122.39662170410156 37.82009043941308,-122.34134674072267 37.714244967649265,-122.36812591552733 37.64495643427851,-122.51129150390625 37.71560291938265))"
}'''

# square around SF
GEOM = '''{
        "type": "Polygon",
        "coordinates": [
          [
            [
              -122.5312042236328,
              37.69631767236258
            ],
            [
              -122.5312042236328,
              37.816564698091184
            ],
            [
              -122.35919952392578,
              37.816564698091184
            ],
            [
              -122.35919952392578,
              37.69631767236258
            ],
            [
              -122.5312042236328,
              37.69631767236258
            ]
          ]
        ]
}'''


class Urthecast():
    @classmethod
    def create(cls, title, geom, start=None, end=None, email=0,
               text=0):

        start, end = cls.parse_dates(start, end)

        params = dict(key=KEY, secret=SECRET)

        payload = json.dumps(cls.gen_payload(title, geom, start, end, email, text))
        headers = {'content-type': 'application/json'}

        r = requests.post(BASEURL, params=params, data=payload, headers=headers)

        return r.json()

    @classmethod
    def parse_dates(cls, start, end):
        if start:
            if type(start) != int:
                msg = 'Start parameter must be seconds since UNIX epoch'
                raise TypeError(msg)
        else:
            start = int(time.mktime(datetime.datetime.now().timetuple()))
        if not end:
            end = start  # per UC API, means indefinite subscription
        return start, end

    @classmethod
    def gen_payload(cls, title, geom, start, end, email, text):
        if email:
            email = 1
        if text:
            text = 1

        # need actual dictionary for wkt conversion
        if type(geom) == str:
            geom = json.loads(geom)
        geom = wkt.dumps(geom)

        payload = dict(title=title, email_notification=email,
                       text_message_notification=text, start_date=start,
                       end_date=end, geometry=geom)

        return payload
print Urthecast.create('SF sub - this is it', geom=GEOM)
