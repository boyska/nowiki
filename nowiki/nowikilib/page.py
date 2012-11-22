from flatdb import FlatDB

class Page:
    @classmethod
    def config(cls, dbpath):
        cls.dbpath = dbpath
        cls.db = FlatDB(dbpath)

    @classmethod
    def get(cls, slug):
        '''Returns the content of the page. If it does not exists,
        raises ValueError'''
        if not cls.exists(slug):
            raise ValueError('page not found')
        return cls.db.get(slug)

    @classmethod
    def set(cls, slug, content):
        '''Set the content of the page to content. If it does not exists,
        raises ValueError'''
        raise NotImplementedError()

    @classmethod
    def create(cls, slug):
        '''Create a page. Returns True if it didn't already exist, else False'''
        raise NotImplementedError()

    @classmethod
    def exists(cls, slug):
        '''Check if a page exists. Returns boolean accordingly'''
        return cls.db.has(slug)
    
    @classmethod
    def get_all_names(cls):
        return tuple(cls.db.keys())

    @classmethod
    def get_all(cls):
        dump = {}
        for slug in cls.get_all_names():
            dump[slug] = Page.get(slug)
        return dump


    def __init__(self, slug=None, content=None):
        self.slug = slug
        self.content = content

    def save(self):
        if not self.slug:
            raise Exception()
        if not self.content:
            raise Exception()
        Page.create(self.slug)
        Page.set(self.slug, self.content)
