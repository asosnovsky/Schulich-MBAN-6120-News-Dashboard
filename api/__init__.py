import pandas as pd

from textblob import TextBlob

from .config import NEWS_API_KEY, NEWS_API_BASE_URL, DB_PATH
from .newsapi import NewsAPI, SortBy, Status, Article, convert_isoformat_to_datetime
from .newsapi import RemoteServerError, WORD_REGEX, STOP_WORDS

newsapi = NewsAPI(NEWS_API_BASE_URL, NEWS_API_KEY, DB_PATH)

def mine_data(topic_to_search: list, verbose: bool = False):
    current_data_dates = newsapi.query_db("""
        SELECT 
            topic,
            MAX(publishedAt) as lastDate,
            MIN(publishedAt) as firstDate
        FROM 
            articles
        GROUP BY `topic`
    """)

    for row in current_data_dates:
        newsapi.update_db_from_remote(row['topic'], fromDate=row['lastDate'], verbose=verbose)

        # remove topic from list
        topic_to_search.pop(
            topic_to_search.index(row['topic'])
        )

    # deal with unfound topics
    for topic in topic_to_search:
        newsapi.update_db_from_remote(topic, verbose=verbose)
        print(f"======== DONE {topic} ========")

def clean_data(verbose: bool = False):
    # Get total Counts
    total_articles = newsapi.query_db("""
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
        return newsapi.query_db("""
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
            if row['title'] is not None:
                for word in row['title'].split(' '):
                    for sub_word in WORD_REGEX.findall(word.lower()):
                        if sub_word not in STOP_WORDS and WORD_REGEX.match(sub_word):
                            if sub_word not in word_counter.keys():
                                word_counter[sub_word] = 0
                            word_counter[sub_word] += 1
            if len(word_counter) > 0:
                newsapi.insert_word_counts(row['obj_id'], row['topic'], word_counter) 
            else:
                # Removes useless articles
                # these are usually non-english articles that somehow snack in
                with newsapi.get_db() as c:
                    c.execute("DELETE FROM articles WHERE obj_id = ?", (row['obj_id'], ) ) 
            processed_count += 1
            if verbose: print(f"Processing ... {processed_count}/{total_articles}")
        rows = get_rows()


def compute_sentiment(verbose: bool = False):
    # Define a function to get data
    def get_rows():
        with newsapi.get_db() as conn:
            return pd.read_sql("""
                SELECT 
                    obj_id,
                    topic, 
                    description, 
                    publishedAt, 
                    content
                FROM
                    articles
                WHERE obj_id NOT IN (
                    SELECT DISTINCT obj_id FROM article_sentiment
                )
                LIMIT 100
            """, conn)

    # Loop on data
    rows = get_rows()
    processed_count = 0
    while len(rows) > 0:
        articles = rows.\
            assign(
                content = rows.content.astype(str),
                description = rows.description.astype(str),
            )
        articles = articles.\
            assign(
                content_sentiment     = articles['content'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity),
                description_sentiment = articles['description'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity),
            )
        articles = articles.\
            assign(
                overall_sentiment = articles[['content_sentiment', 'description_sentiment']].mean(axis=1)
            )
        newsapi.insert_sentiment(articles)
        processed_count += len(articles)
        rows = get_rows()
        if verbose: print(f"Processsed {processed_count}")