import json
import logging
from kigo.etl.runtime.registry import MappingRegistry
from kigo.etl.mapper.mapping import MappingInfo


class Config:
    __config = {}

    @classmethod
    def load(cls, file_path):
        with open(file_path, "r") as f:
            Config.__config = json.load(f)
        Config.clean()
        Config.validate()
        Config.merge()
        return Config()

    @property
    def config(self):
        return Config.__config

    @property
    def mapping(self):
        return Mapping(Config.__config["mapping"])

    @classmethod
    def clean(cls):
        for conf in Config.__config["mapping"]:
            cname = next(iter(conf["class"]))
            mapping_info = MappingRegistry.mappings[cname]
            mapping_info.clazz[1] = {}
            mapping_info.readers = []

    @classmethod
    def merge(cls):
        for conf in Config.__config["mapping"]:
            cname = next(iter(conf["class"]))
            cparams = conf["class"][cname]
            mapping_info = MappingRegistry.mappings[cname]
            if not mapping_info.clazz[1]:
                mapping_info.clazz[1] = cparams
            if not mapping_info.readers:
                for reader in conf["readers"]:
                    rname = next(iter(reader))
                    rparams = reader[rname]
                    mapping_info.readers.append((MappingRegistry.readers[rname], rparams))

    @classmethod
    def validate(cls):
        if len(Config.__config["mapping"]) != len(MappingRegistry.mappings):
            logging.warning(f"The number of mappings does not match the configuration! Configuration mappings: {len(Config.__config['mapping'])} ETL definitions {len(MappingRegistry.mappings)}")

        for conf in Config.__config["mapping"]:
            cname = next(iter(conf["class"]))
            if not cname in MappingRegistry.mappings:
                logging.error(f"The class <{cname}> is not exist in ETL definition!")
            for reader in conf["readers"]:
                rname = next(iter(reader))
                if not rname in MappingRegistry.readers:
                    logging.error(f"The reader <{cname}> is not exist in ETL definition!")

    def __repr__(self):
        return json.dumps(Config.__config)


class Mapping:
    def __init__(self, mapping):
        self._iter_pos = 0
        self.mapping = mapping

    def __repr__(self):
        return str(self.mapping)

    def __next__(self) -> MappingInfo:
        if not self._iter_pos < len(self.mapping):
            raise StopIteration

        conf = self.mapping[self._iter_pos]
        cname = next(iter(conf["class"]))
        mapping_info = MappingRegistry.mappings[cname]
        self._iter_pos += 1

        return mapping_info

    def __iter__(self):
        self._iter_pos = 0
        return self






