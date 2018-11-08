# configure nltk
import nltk
nltk.download('stopwords')

# Dependencies
import sqlite3
import json
import math
import logging

# Deps
import re

from typing import List
from nltk.corpus import stopwords

from .NewsDB import NewsDB
from .NewsAPIRemote import NewsAPIRemote, Request, Response, Status, SortBy, Article
from .util import dict_factory, convert_isoformat_to_datetime

log = logging.getLogger(__name__)

STOP_WORDS = set(stopwords.words('english')) 
WORD_REGEX = re.compile("[A-Za-z]+")

class RemoteServerError(Exception):
    def __init__(self, res: Response):
        self.res = res
        Exception.__init__(self, res.message)

class NewsAPI(NewsDB):
    def __init__(self, baseUrl: str, apiKey: str, dbLocation: str = ":memory:"):
        NewsDB.__init__(self, dbLocation)
        self._remote = NewsAPIRemote(baseUrl, apiKey)

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
            raise RemoteServerError(response_obj)
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
                if res.status == Status.ERROR:
                    raise RemoteServerError(res)
                self.insert_article(res.articles, q)
        if verbose:
            logging.basicConfig(level=logging.WARNING)

