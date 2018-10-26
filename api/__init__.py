from .config import NEWS_API_KEY, NEWS_API_BASE_URL, DB_PATH
from .newsapi import NewsAPI, SortBy, Status, Article, convert_isoformat_to_datetime

newsapi = NewsAPI(NEWS_API_BASE_URL, NEWS_API_KEY, DB_PATH)