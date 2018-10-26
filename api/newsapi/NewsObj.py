from enum import Enum

def repr_val(key: str, val):
    if isinstance(val, list):
        return f'{key}="Array<dict({len(val)})>"'
    if isinstance(val, dict):
        return f'{key}="Dict<{len(val)}>"'
    if isinstance(val, Enum):
        return f'{key}="{val.value}"'
    return f'{key}="{val}"'

class NewsObj:
    def __init__(self, **kwargs):
        self._data = kwargs
    
    def __getattr__(self, attr: str):
        if attr in self._data.keys():
            return self._data[attr]
        raise AttributeError

    @classmethod
    def from_json(cls, json: dict):
        return cls(**json)

    def __repr__(self) -> str:
        return f'''<{self.__class__.__name__} {" ".join([
            repr_val(key, val)
            for key, val in self._data.items()
        ])} />'''