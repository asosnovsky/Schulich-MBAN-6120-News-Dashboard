import threading

from api import mine_data, clean_data, compute_sentiment
from api import RemoteServerError
from constants import DEFAULT_TOPIC_LIST

class UpdateThread(threading.Thread):
    def __init__(self, verbose: bool = False):
        threading.Thread.__init__(self)
        self.verbose = verbose
    def run(self):
        from time import sleep
        while True:
            try:
                mine_data(DEFAULT_TOPIC_LIST, self.verbose)
                clean_data(self.verbose)
                compute_sentiment(self.verbose)
                sleep(5)
            except RemoteServerError as e:
                print("NEWSAPI::", e.res.message)
                clean_data(self.verbose)
                compute_sentiment(self.verbose)
                print("Sleeping for 6-hours")
                sleep(6 * 60 * 60)

def launch(verbose: bool = False):
    t = UpdateThread(verbose)
    t.start()

if __name__ == "__main__":
    launch(True)
