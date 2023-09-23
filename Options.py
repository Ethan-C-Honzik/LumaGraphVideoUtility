import inspect
import json


class Options:
    def __init__(self):
        self.frameRate = 24
        self.height = 256
        self.width = 256

    @classmethod
    def from_dict(cls, data):
        instance = cls.__new__(cls)
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)
