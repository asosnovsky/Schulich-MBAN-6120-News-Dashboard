# Schulich-MBAN-6120-News-Dashboard
WIP

# Setup

- clone repo
- install python 3.6+
- get a news api key from [here](https://newsapi.org/)
- copy the file `api/example_secrets.py` into `api/_secrets.py`
- put your api key in `api/_secrets.py`

# Populate Database
- run `python data_miner.py` to populate database
- run `python data_cleaner.py` to generate word counts in db

# Run webapp
- install [node-js](https://nodejs.org/en/)
- go to `/static`, run `npm i`, this will create your `node_modules` folder
- run `python rest_api.py` to run the web-app