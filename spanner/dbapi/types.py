# Copyright 2019 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Implements the types requested by the Python Database API in:
#   https://www.python.org/dev/peps/pep-0249/#type-objects-and-constructors

import datetime
import time


def Date(year, month, day):
    return datetime.date(year, month, day)


def Time(hour, minute, second):
    return datetime.time(hour, minute, second)


def Timestamp(year, month, day, hour, minute, second):
    return datetime.datetime(year, month, day, hour, minute, second)


def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


def Binary(string):
    """
    Creates an object capable of holding a binary (long) string value.
    """
    return BINARY(string)


class BINARY(object):
    """
    This object describes (long) binary columns in a database (e.g. LONG, RAW, BLOBS).
    """
    # TODO: Implement me.
    pass


class STRING(object):
    """
    This object describes columns in a database that are string-based (e.g. CHAR).
    """
    # TODO: Implement me.
    pass


class NUMBER(object):
    """
    This object describes numeric columns in a database.
    """
    # TODO: Implement me.
    pass


class DATETIME(object):
    """
    This object describes date/time columns in a database.
    """
    # TODO: Implement me.
    pass


class ROWID(object):
    """
    This object describes the "Row ID" column in a database.
    """
    # TODO: Implement me.
    pass