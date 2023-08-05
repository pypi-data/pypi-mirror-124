__all__ = []

import abc
from enum import Enum

class ReaderType(Enum):
    ABC  = "ABC"
    TEXT = "TEXT"
    CSV  = "CSV"
    XML  = "XML"
    JSON = "JSON"

class FileReader(abc.ABC):

    __reader_type__ = ReaderType.ABC

    @abc.abstractmethod
    def __init__(self, path):
        self.path = path
        self.__reader = None

    def __iter__(self):
        self.__reader = self.read()
        return self

    def __next__(self):
        is_correct = False
        while not is_correct:
            num, data = next(self.__reader)
            if self.on_read(num, data):
                is_correct = True
        return num, data


    @classmethod
    @property
    def type(clr) -> ReaderType:
        return clr.__reader_type__

    @abc.abstractmethod
    def read(self):
        with open(self.path, "r") as f:
            for num, line in enumerate(f):
                yield num, line

    def on_read(self, num, data) -> bool:
        """
        For each consistent piece of examples.
        If False is returned, the examples fragment will be skipped
        :return:
        """
        return True
