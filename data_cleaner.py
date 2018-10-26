# configure nltk
# import nltk
# nltk.download('stopwords')

# Deps
import re

from nltk.corpus import stopwords
from pprint import pprint

from api import newsapi

newsapi.update_db_word_counter(verbose=True)
