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

"""This module supports acessing TERRAI data."""

from gfw.forestchange.common import CartoDbExecutor
from gfw.forestchange.common import Sql


class TerraiSql(Sql):

    WORLD = """
        TODO"""

    ISO = """
        TODO"""

    ID1 = """
        TODO"""

    WDPA = """
        TODO"""

    USE = """
        TODO"""

    @classmethod
    def download(cls, sql):
        return ' '.join(
            sql.replace("SELECT COUNT(f.*) AS value", "SELECT f.*").split())


def _processResults(action, data):
    """The data param is a JSON CartoDB response object."""
    if 'rows' in data:
        result = data['rows'][0]
        data.pop('rows')
    else:
        result = dict(value=None)

    data['value'] = result['value']

    return action, data


def execute(args):
    args['version'] = 'v2'
    action, data = CartoDbExecutor.execute(args, TerraiSql)
    if action == 'redirect' or action == 'error':
        return action, data
    return _processResults(action, data)
