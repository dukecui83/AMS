#!/usr/bin/env python
# coding: utf-8

from time import time
from ams.structures import CLIENT


class Kvs(object):

    @staticmethod
    def get_timestamp_string(timestamp=None):
        if timestamp is None:
            timestamp = time()
        return str(int(1000.0*timestamp))

    @staticmethod
    def get_key_timestamp(key):
        return key.split(CLIENT.KVS.KEY_PATTERN_DELIMITER)[-1]

    @staticmethod
    def get_key_from_timestamped_key(timestamped_key):
        return CLIENT.KVS.KEY_PATTERN_DELIMITER.join(timestamped_key.split(CLIENT.KVS.KEY_PATTERN_DELIMITER)[:-1])

    @staticmethod
    def delete_old_keys_and_get_latest_key(keys, delete_function):
        sorted_keys = sorted(keys, key=lambda x: int(Kvs.get_key_timestamp(x)))
        try:
            list(map(delete_function, sorted_keys[:-1]))
        except KeyError:
            pass
        return sorted_keys[-1] if 0 < len(sorted_keys) else None
