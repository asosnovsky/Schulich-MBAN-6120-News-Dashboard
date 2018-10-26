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
    pass

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
        if verbose:
            logging.basicConfig(level=logging.WARNING)

    def update_db_word_counter(self, verbose: bool = False):
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        
        # Get total Counts
        total_articles = self.query_db("""
            SELECT 
                COUNT() AS N
            FROM
                articles
            WHERE obj_id NOT IN (
                SELECT DISTINCT obj_id FROM word_counts
            )
        """)[0]["N"]

        # Define a function to get data
        def get_rows():
            return self.query_db("""
                SELECT 
                    obj_id, 
                    topic,
                    title 
                FROM
                    articles
                WHERE obj_id NOT IN (
                    SELECT DISTINCT obj_id FROM word_counts
                )
                LIMIT 100
            """)

        # Loop on data
        rows = get_rows()
        processed_count = 0
        while len(rows) > 0:
            for row in rows:
                word_counter = {}
                for word in row['title'].split(' '):
                    for sub_word in WORD_REGEX.findall(word.lower()):
                        if sub_word not in STOP_WORDS and WORD_REGEX.match(sub_word):
                            if sub_word not in word_counter.keys():
                                word_counter[sub_word] = 0
                            word_counter[sub_word] += 1
                self.insert_word_counts(row['obj_id'], row['topic'], word_counter)  
            processed_count += len(rows)
            rows = get_rows()
            log.info(f"Processing ... {processed_count}/{total_articles}")

        if verbose:
            logging.basicConfig(level=logging.WARNING)
