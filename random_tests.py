from api import newsapi


with newsapi.get_db() as cur:
    cur.execute("drop table word_counts")
    cur.commit()
    