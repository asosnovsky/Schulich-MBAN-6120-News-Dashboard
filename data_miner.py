from api import newsapi, Article

# articles = newsapi.query_remote("bitcoin", "abc-remote")

topic_to_search = [
    'btc', 
    'bitcoin',
    'crypto',
    'etherium'
]

current_data_dates = newsapi.query_db("""
    SELECT 
        topic,
        MAX(publishedAt) as lastDate,
        MIN(publishedAt) as firstDate
    FROM 
        articles
    GROUP BY `topic`
""")

print(current_data_dates)
for row in current_data_dates:
    newsapi.update_db_from_remote(row['topic'], fromDate=row['lastDate'], verbose=True)

    # remove topic from list
    topic_to_search.pop(
        topic_to_search.index(row['topic'])
    )
# deal with unfound topics
for topic in topic_to_search:
    newsapi.update_db_from_remote(topic, verbose=True)
    print(f"======== DONE {topic} ========")





# current_data_dates = newsapi.query_db("""
#     SELECT 
#         MAX(publishedAt) as lastDate,
#         MIN(publishedAt) as firstDate
#     FROM 
#         articles
# """)[0]

# print(current_data_dates)