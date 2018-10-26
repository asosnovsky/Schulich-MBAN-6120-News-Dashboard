from enum import Enum
from typing import List
from .NewsObj import NewsObj
from .Article import Article

class Status(Enum):
    OK = 'ok'
    ERROR = 'error'

    @classmethod
    def from_str(cls, s: str):
        for v in cls:
            if v.value == s:
                return v
        raise Exception("Invalid Status")

class Response(NewsObj):
    def __init__(self, 
        status: Status, 
        totalResults: int = 0, 
        articles: List[Article] = 0,
        code: str = None,
        message: str = None,
    ):
        NewsObj.__init__(self,
            status=status, 
            totalResults=totalResults,
            articles=articles,
            code=code,
            message=message
        )
    
    @classmethod
    def from_json(cls, json: dict):
        return Response(**{
            **json,
            'articles': [
                Article.from_json(row)
                for row in json['articles']
            ] if 'articles' in json else [],
            'status': Status.from_str(json['status'])
        })
