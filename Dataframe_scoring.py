import pandas as pd
import sqlite3
from textblob import TextBlob


conn = sqlite3.connect('db.db')

df= pd.read_sql("SELECT topic, description, publishedAt, content "
               "FROM articles "
               "where topic = 'terrorism'", conn)

#Convert column to string for TextBlob Sentiment Analysis
df.content = df.content.astype(str)
df.description = df.description.astype(str)

df['content_sentiment'] = df['content'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity)
df['description_sentiment'] = df['description'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity)
df['total_sentiment'] = df['content_sentiment'] + df['description_sentiment']
df['sentiment'] = 0


# THRESHOLDS
positive = 0.2
# neutral_threshold = [-0.2 - 0.2]
negative= - 0.2

for i in range(0, len(df)):
    if df['total_sentiment'][i] > positive:
        df.iloc[i, df.columns.get_loc('sentiment')] = 1
    elif df['total_sentiment'][i] < negative:
        df.iloc[i, df.columns.get_loc('sentiment')] = -1
    else:
        df.iloc[i, df.columns.get_loc('sentiment')] = 0

# print (df)
# df.to_csv('myfile.csv')