# Schulich-MBAN-6120-News-Dashboard
WIP

<img src="readme-assets/eg2.gif">

# Setup

- clone repo
- install python 3.6+
- get a news api key from [here](https://newsapi.org/)
- copy the file `api/example_secrets.py` into `api/_secrets.py`
- put your api key in `api/_secrets.py`

# Populate Database
- run `python data_updater.py` to run a process that updates the database every 5s

# Run Web App
- run `python rest_api.py` to run the web-app

# Run main process
- run `python main.py`