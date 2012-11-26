from __future__ import with_statement

import os, os.path
import fcntl
import stat, grp

class FlatDB(object):
    def __init__(self, config):
        self.config = config
        self.path = config.get('nowiki', 'datapath')

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

    def check_sanity(self, fix=False):
        '''
        check user/permissions on the dir
        
        fix determine if it just has to report or errors or fix them

        returns False if errors were detected, True if everything is file
        '''
        wanted_permission = self.config.get('nowiki', 'permission')
        wanted_group = grp.getgrnam(self.config.get('nowiki', 'group')).gr_gid
        _err = False
        for name in self.keys():
            path = os.path.join(self.path, name)
            stat = os.stat(path)
            if oct(stat.st_mode)[-3:] != wanted_permission:
                if fix:
                    os.chmod(path, int(wanted_permission, 8))
                _err = True
            if os.stat(path).st_gid != wanted_group:
                if fix:
                    uid = os.stat(path).st_uid
                    os.chown(path, uid, wanted_group)
                _err = True
        return not _err
                

