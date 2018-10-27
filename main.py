import data_updater
import rest_api

data_updater.launch()

rest_api.app.run(
    port="8080"
)