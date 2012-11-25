from __future__ import with_statement

import os, os.path
import fcntl

class FlatDB(object):
    def __init__(self, path):
        self.path = path

    def keys(self):
        all_in_dir = os.listdir(self.path)
        for name in all_in_dir:
            if not FlatDB.is_valid_key(name):
                continue
            fullname = os.path.join(self.path, name)
            if os.path.isfile(fullname) and not os.path.islink(fullname):
                yield name

    @staticmethod
    def is_valid_key(key):
        return key.isalnum()

    def has(self, key):
        if not FlatDB.is_valid_key(key):
            raise ValueError()
        return os.path.exists(os.path.join(self.path, key))

    def create(self, key):
        if not FlatDB.is_valid_key(key):
            raise ValueError()
        if not self.has(key):
            open(os.path.join(self.path, key), 'w')

    def set(self, key, value):
        if not FlatDB.is_valid_key(key):
            raise ValueError()
        with open(os.path.join(self.path, key), 'w') as buf:
            buf.write(value)
    
    def get(self, key):
        if not FlatDB.is_valid_key(key):
            raise ValueError()
        with open(os.path.join(self.path, key), 'r') as buf:
            fcntl.flock(buf.fileno(), fcntl.LOCK_SH)
            content = buf.read()
            fcntl.flock(buf.fileno(), fcntl.LOCK_UN)
            return content

    def delete(self, key):
        if not FlatDB.is_valid_key(key):
            raise ValueError()
        os.remove(os.path.join(self.path, key))
