import json

from .NewsObj import NewsObj
from .util import dict_factory, sqlite3, datetime, convert_isoformat_to_datetime

class Article(NewsObj):
    def __init__(self,
        source: dict,
        author: str,
        title: str,
        description: str,
        url: str,
        urlToImage: str,
        publishedAt: datetime or str,
        content: str,
        topic: str = None,
        obj_id: str = None,
    ): 
        if isinstance(publishedAt, str):
            publishedAt = convert_isoformat_to_datetime(publishedAt)
        NewsObj.__init__(
            self,
            obj_id=obj_id,
            topic=topic,
            source=source,
            author=author,
            title=title,
            description=description,
            url=url,
            urlToImage=urlToImage,
            publishedAt=publishedAt,
            content=content
        )
        if obj_id is None:
            self.remake_obj_id()

    def remake_obj_id(self) -> str:
        self._data['obj_id'] = f"{self.topic}/{self.source['id']}/{self.source['name']}/{self.author}/{self.title}/{self.publishedAt}"
        return self.obj_id
    
    def set_topic(self, val: str):
        self._data['topic'] = val
        self.remake_obj_id()
    
    def set_topic_return_list(self, newtopic: str, colnames: list, as_tupple: bool = False) -> (list or tuple):
        self.set_topic(newtopic)
        if as_tupple:
            return self.to_tupple(colnames)
        return self.to_list(colnames)

    def to_list(self, colnames = [ 'obj_id', 'topic', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content' ]) -> list:
        ret_value = []
        for colname in colnames:
            if colname == 'source':
                ret_value.append(
                    json.dumps(self.source)
                )
            elif colname == 'publishedAt':
                ret_value.append(
                    self.publishedAt.isoformat()
                )
            else:
                ret_value.append(self.__getattr__(colname))
        return ret_value
    
    def to_tupple(self, colnames = [ 'obj_id', 'topic', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content' ] ) -> tuple:
        return (*self.to_list(colnames),)

    @classmethod
    def from_json(cls, obj: dict):
        if isinstance(obj['source'], str):
            obj['source'] = json.loads(obj['source'])
        return Article(**obj)

    @classmethod
    def from_cursor_row(cls, cursor: sqlite3.Cursor, row: tuple):
        return Article.from_json(dict_factory(cursor, row))
    