#!/usr/bin/env python3
#
# Copyright (C) 2022 Rackslab
#
# This file is part of RacksDB.
#
# RacksDB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RacksDB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RacksDB.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import yaml
import sys

from .version import __version__
from .types import RacksDBTypes
from .types.node import RacksDBNodeType
from .errors import RacksDBFormatError, RacksDBSchemaError
from .schema import Schema
from .db import GenericDB


class RacksDBExec:
    @classmethod
    def run(cls):
        cls()

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Do something with RacksDB.'
        )
        parser.add_argument(
            '-v',
            '--version',
            dest='version',
            action='version',
            version='RacksDB ' + __version__,
        )
        parser.add_argument(
            '--debug',
            dest='debug',
            action='store_true',
            help="Enable debug mode",
        )

        parser.add_argument(
            '-s',
            '--schema',
            help="Schema to load",
            required=True,
        )
        parser.add_argument(
            '-b',
            '--db',
            help="Database to load",
            required=True,
        )

        self.args = parser.parse_args()

        self.types = RacksDBTypes()

        self._run()

    def _run(self):

        try:
            schema = Schema.load(self.args.schema)
        except RacksDBSchemaError as err:
            print(f"Error while loading schema: {err}")
            sys.exit(1)
        schema.dump()

        try:
            db = GenericDB.load('RacksDB', self.args.db, schema)
        except RacksDBFormatError as err:
            print(f"Error while loading db: {err}")
            sys.exit(1)

        db.dump()
