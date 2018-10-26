import sqlite3

from typing import List, Dict

from .NewsAPIRemote import Article
from .util import dict_factory

class NewsDB:
    def __init__(self, dbLocation: str = ":memory:"):
        self._dbLocation = dbLocation
        self.create_db()

    def get_db(self):
        return sqlite3.connect(self._dbLocation)

    def create_db(self):
        with self.get_db() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    obj_id String Primary Key,
                    topic String,
                    source String,
                    author String,
                    title String,
                    description String,
                    url String,
                    urlToImage String,
                    publishedAt Datetime,
                    content String
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS word_counts (
                    obj_id String,
                    topic String,
                    word String,
                    count Integer,
                    
                    Primary Key (obj_id, topic, word)
                );
            """)
            cursor.commit()

    def query_db(self, sql_code: str, *params, mapping_function=dict_factory):
        with self.get_db() as cursor:
            cursor_exc = cursor.execute(sql_code, (*params,))
            data = [
                mapping_function(cursor_exc, row)
                for row in cursor_exc
            ]
        return data

    def insert_article(self, articles: List[Article], topic: str = None):
        col_names = [
            "obj_id",
            "source",
            "author",
            "title",
            "description",
            "url",
            "urlToImage",
            "publishedAt",
            "content",
        ]
        if topic is not None:
            col_names.append('topic')
        data = ( article.set_topic_return_list(topic, col_names) for article in articles ) 

        with self.get_db() as cursor:
            cursor.executemany(
                f"""
                    INSERT OR IGNORE INTO articles ({ ','.join(col_names) })
                    VALUES 
                    ({ ",".join( 
                        ["?"] * len(col_names) 
                    ) })
                """, 
                data
            )
            cursor.commit()

    def insert_word_counts(self, obj_id: str, topic:str, word_counter: Dict[str, int]):
        with self.get_db() as cursor:
            cursor.executemany(
                """
                    INSERT INTO 
                        word_counts (obj_id, topic, word, count) 
                    VALUES (?, ?, ?, ?)
                """,
                (
                    ( obj_id, topic, key, value )
                    for key, value in word_counter.items()
                )
            )   
            cursor.commit()  