from api import newsapi
from pprint import pprint

pprint(
    newsapi.query_db(""" 
        SELECT 
            topic, 
            word as text, 
            COUNT() as size
        FROM word_counts
        GROUP BY topic, word
    """)
)
