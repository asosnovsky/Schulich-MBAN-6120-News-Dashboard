import json

from api import newsapi
from api.newsapi.util import dict_factory

from pprint import pprint

def mapping_function(c, row):
    obj = dict_factory(c, row)
    json_source = json.loads(obj['source'])
    obj['source'] = json_source['name'] if json_source['name'] else json_source['id']
    return obj

pprint(
    newsapi.query_db(""" 
        SELECT 
            topic, source, 
            COUNT() as size
        FROM articles
        WHERE topic = 'trump'
        GROUP BY topic, source
        HAVING size > 2
    """, mapping_function=mapping_function)
)
