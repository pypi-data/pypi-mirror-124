__all__ = ['Loader', 'NullLoader']

import warnings


class Loader:
    model = None
    serializer_class = None

    def __init__(self, source=None):
        self.source = source

    def load(self):
        if not self.source or not self.serializer_class:
            return

        for raw_data in self.source:
            data = self.parse(raw_data)
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                continue
                # TODO: warnings.warn()
            serializer.save()

    def parse(self, raw_data):
        return raw_data


class NullLoader(Loader):
    def load(self):
        return