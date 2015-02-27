import json
import unittest

from gfw.pubsub.urthecast import Urthecast

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


class Test(unittest.TestCase):
    def test_parse_dates(self):
        start = '2015-01-01'
        end = '2015-02-01'

        result = Urthecast.parse_dates(start, end)
        # checked on epochconverter.com
        expected = (1420070400, 1422748800)

        self.assertEqual(result, expected)

    def test_parse_dates_noend(self):
        start = '2015-01-01'

        result = Urthecast.parse_dates(start)
        # checked on epochconverter.com
        expected = (1420070400, 1420070400)

        self.assertEqual(result, expected)

    def test_parse_dates_nodate(self):
        result = Urthecast.parse_dates()
        self.assertEqual(result[0], result[1])

    def test_create(self):
        title = 'test'
        geom = GEOM
        start = 2015-01-01
        end = 2016-01-01

        response = Urthecast.create(title, geom, start, end)
        result = response['status']
        expected = 201

        self.assertEqual(result, expected)

    def test_create_badgeom(self):
        title = 'test'
        geom = None
        start = 2015-01-01
        end = 2016-01-01

        response = Urthecast.create(title, geom, start, end)
        result = response['status']
        expected = 400

        self.assertEqual(result, expected)

    @unittest.skip("Haven't figured out notifications yet")
    def test_notifications(self):
        subid = 398  # previously created
        result = Urthecast.notifications(subid)
        expected = None

        self.assertEqual(result, expected)

    def test_delete(self):
        """Create a subscription, then delete it."""
        title = 'test'
        geom = GEOM
        start = 2015-01-01
        end = 2016-01-01

        response = Urthecast.create(title, geom, start, end)
        subid = response['payload'][0]['id']

        result = Urthecast.delete(subid)['status']
        expected = 200

        self.assertEqual(result, expected)
