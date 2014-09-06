# coding: utf-8

from datetime import datetime
from time import mktime


def timestamp_to_datetime(timestamp):
    if isinstance(timestamp, (str, unicode)):
        if len(timestamp) == 13:
            timestamp = int(timestamp) / 1000
        return datetime.fromtimestamp(timestamp)
    return ""


def datetime_to_timestamp(date):
    if isinstance(date, datetime):
        timestamp = mktime(date.timetuple())
        json_timestamp = int(timestamp) * 1000

        return '{0}'.format(json_timestamp)
    return ""
