import datetime
import time
import json
import os
import calendar

import requests

SUBURL = 'https://api.urthecast.com/v1/apps/subscriptions/'
NOTIFYURL = 'https://api.urthecast.com/v1/apps/notifications/'
KEY = os.environ['URTHECAST_KEY']
SECRET = os.environ['URTHECAST_SECRET']


class Urthecast():
    @classmethod
    def parse_dates(cls, start=None, end=None):
        if start:
            if type(start) != int:
                start = calendar.timegm(time.strptime(start, '%Y-%m-%d'))
            if not end:
                end = start
            else:
                if type(end) != int:
                    end = calendar.timegm(time.strptime(end, '%Y-%m-%d'))
        else:
            start = int(time.mktime(datetime.datetime.now().timetuple()))
            end = start
        return start, end

    @classmethod
    def _gen_payload(cls, title, geom, start, end, email, text):
        if email:
            email = 1
        if text:
            text = 1

        payload = dict(title=title, email_notification=email,
                       text_message_notification=text, start_date=start,
                       end_date=end, geometry=geom)

        return payload

    @classmethod
    def create(cls, title, geom, start=None, end=None, email=0,
               text=0):

        start, end = cls.parse_dates(start, end)

        params = dict(key=KEY, secret=SECRET)

        payload = cls._gen_payload(title, geom, start, end, email, text)
        payload = json.dumps(payload)
        headers = {'content-type': 'application/json'}

        response = requests.post(SUBURL, params=params, data=payload,
                                 headers=headers)
        return response.json()

    @classmethod
    def notifications(cls, subid=None):
        params = dict(key=KEY, secret=SECRET)
        if subid:
            url = os.path.join(NOTIFYURL, str(subid))
        else:
            url = os.path.join(NOTIFYURL)
        r = requests.get(url, params=params)

        return cls.parse_notifications(r.json(), subid)

    @classmethod
    def delete(cls, subid):
        params = dict(key=KEY, secret=SECRET)
        url = os.path.join(SUBURL, str(subid))
        return requests.delete(url, params=params).json()
