# configure nltk
# import nltk
# nltk.download('stopwords')

# Deps
import re

from nltk.corpus import stopwords
from pprint import pprint

from api import newsapi

def clean_data(verbose: bool = False):
    newsapi.update_db_word_counter(verbose=verbose)

if __name__ == "__main__":
    clean_data(True)