import data_updater
import rest_api

# start data updater
data_updater.launch()

# Run application
rest_api.app.run(
    port="8080"
)