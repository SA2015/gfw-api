# Global Forest Watch API
# Copyright (C) 2014 World Resource Institute
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Unit test coverage for gfw.forestchange.args"""

import json
import unittest

from google.appengine.ext import testbed

from gfw.forestchange import args


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()


class ArgsTest(BaseTest):

    def test_period(self):
        f = args.ArgProcessor.period
        begin = '2000-01-01'
        end = '2014-01-01'
        for x in ['%s,%s' % (begin, end)]:
            self.assertEqual(f(x)['begin'], begin)
            self.assertEqual(f(x)['end'], end)

        with self.assertRaises(args.PeriodArgError):
            f('2000-01-02')
        with self.assertRaises(args.PeriodArgError):
            f('2000-01-02,')
        with self.assertRaises(args.PeriodArgError):
            f(',2000-01-02')
        with self.assertRaises(args.PeriodArgError):
            f('2000-1-2,1999-1-2')  # begin > end

    def test_geojson(self):
        f = args.ArgProcessor.geojson
        arg = '{"type": "Polygon"}'
        self.assertEquals(f(arg)['geojson'], arg)
        arg = '{"type": "MultiPolygon"}'
        self.assertEquals(f(arg)['geojson'], arg)
        with self.assertRaises(args.GeoJsonArgError):
            f(json.dumps({"type": "Line"}))  # Wrong type
        with self.assertRaises(args.GeoJsonArgError):
            f('{"type": Polygon}')  # Invalid JSON

    def test_download(self):
        f = args.ArgProcessor.download
        arg = 'foo.csv'
        self.assertEqual(f(arg)['format'], 'csv')
        self.assertEqual(f(arg)['filename'], 'foo')
        with self.assertRaises(args.DownloadArgError):
            f('foo')

    def test_use(self):
        f = args.ArgProcessor.use
        for arg in ['logging,1', 'mining,1', 'oilpalm,1', 'fiber,1']:
            self.assertEqual(f(arg)['use'], arg.split(',')[0])
            self.assertEqual(f(arg)['use_pid'], arg.split(',')[1])
        with self.assertRaises(args.UseArgError):
            f('logging')

    def test_bust(self):
        f = args.ArgProcessor.bust
        self.assertTrue(f('bust')['bust'])

    def test_dev(self):
        f = args.ArgProcessor.dev
        self.assertTrue(f('dev')['dev'])

    def test_process(self):
        f = args.ArgProcessor.process
        params = {
            "period": "2007-1-1,2008-1-1",
            "bust": "",
            "dev": "",
            "use": "logging,1",
            "download": "foo.csv",
            "geojson": '{"type": "Polygon"}'
        }
        x = f(params)
        self.assertItemsEqual(
            ['begin', 'end', 'use', 'use_pid', 'filename', 'format',
                'geojson', 'dev', 'bust'],
            x)

if __name__ == '__main__':
    reload(args)
    unittest.main(exit=False)