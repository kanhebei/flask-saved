from collections import namedtuple


class BaseStorage:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Result = namedtuple('Result', 'url flag')
    
    def generate_url(self, filename):
        raise NotImplementedError

    def read(self, filename):
        raise NotImplementedError

    def save(self, f, filename):
        raise NotImplementedError

    def delete(self, filename):
        raise NotImplementedError