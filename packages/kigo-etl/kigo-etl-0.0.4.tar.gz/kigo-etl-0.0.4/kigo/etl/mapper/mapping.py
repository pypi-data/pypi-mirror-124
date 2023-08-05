from kigo.etl.runtime.registry import MappingRegistry


class MappingInfo:
    def __init__(self, clazz, params = {}):
        self._clazz = [clazz, params]
        self._readers = []

    @property
    def readers(self):
        return self._readers

    @property
    def clazz(self):
        return self._clazz

    @readers.setter
    def readers(self, readers):
        self._readers = readers

    def __repr__(self):
        return f"MappingInfo <{self._clazz}> readers: {self._readers}>"


def mapping(clazz):
    MappingRegistry.append_mapping(MappingInfo(clazz))
    return clazz