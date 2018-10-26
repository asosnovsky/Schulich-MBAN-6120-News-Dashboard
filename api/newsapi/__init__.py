import sqlite3
import json
import math
import logging

from typing import List

from .NewsAPIRemote import NewsAPIRemote, Request, Response, Status, SortBy, Article
from .util import dict_factory, convert_isoformat_to_datetime

log = logging.getLogger(__name__)

class RemoteServerError(Exception):
    pass

class NewsAPI:
    def __init__(self, baseUrl: str, apiKey: str, dbLocation: str = ":memory:"):
        self._remote = NewsAPIRemote(baseUrl, apiKey)
        self._db = sqlite3.connect(dbLocation)
        self.create_db()

    def create_db(self):
        cursor = self._db.cursor()
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
        self._db.commit()
        cursor.close()

    def query_db(self, sql_code: str, *params, mapping_function=dict_factory):
        cursor = self._db.execute(sql_code, (*params,))
        return [
            mapping_function(cursor, row)
            for row in cursor
        ]

    def insert_article(self, articles: List[Article], topic: str = None):
        cursor = self._db.cursor()
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
        self._db.commit()
        cursor.close()

    def update_db_from_remote(self, 
        q: str,
        sources: str = None,
        fromDate: str = None,
        toDate: str = None,
        sortBy: SortBy = SortBy.PUBLISH,
        pageSize:int = 100,
        verbose: bool = False
    ):
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        # Request First Page
        request_obj = self._remote.create_request(
            q,
            sources,
            fromDate,
            toDate,
            sortBy,
            pageSize,
            page=1
        ) 
        log.info(f"Processing {request_obj} 1/?")
        response_obj = self._remote.process_request(request_obj)
        if response_obj.status == Status.ERROR:
            log.warn(request_obj, response_obj)
            raise RemoteServerError(response_obj.message)
        self.insert_article(response_obj.articles, q)

        # Count how many pages we should have
        totalPages = math.ceil(response_obj.totalResults/pageSize)

        if totalPages > 1:
            log.info(f"Total pages = {totalPages}")
            for pageNum in range(2, totalPages+1):
                req = self._remote.create_request(
                    q,
                    sources,
                    fromDate,
                    toDate,
                    sortBy,
                    pageSize,
                    page=pageNum
                )
                log.info(f"Processing {req} {pageNum}/{totalPages}")
                res = self._remote.process_request(req)
                if response_obj.status == Status.ERROR:
                    log.warn(req, res)
                    raise RemoteServerError(response_obj.message)
                self.insert_article(response_obj.articles, q)

        
    