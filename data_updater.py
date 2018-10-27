import threading

from data_miner import mine_data
from data_cleaner import clean_data
from api import RemoteServerError

topics = [
    'btc', 
    'bitcoin',
    'crypto',
    'etherium',
    'terrorism',
    'trump'
]

class UpdateThread(threading.Thread):
    def __init__(self, verbose: bool = False):
        threading.Thread.__init__(self)
        self.verbose = verbose
    def run(self):
        from time import sleep
        while True:
            try:
                mine_data(topics, self.verbose)
                clean_data(self.verbose)
                sleep(5)
            except RemoteServerError as e:
                print("NEWSAPI::", e.res.message)
                clean_data(self.verbose)
                print("Sleeping for 6-hours")
                sleep(6 * 60 * 60)

def launch(verbose: bool = False):
    t = UpdateThread(verbose)
    t.start()

if __name__ == "__main__":
    launch(True)
