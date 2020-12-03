import requests
import configparser
from core_connect import Core
import json

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Set the proxy to Call the Microsoft Teams WebHook
proxyDict = {
        'http': 'http://proxy:8080',
        'https': 'http://proxy:8080'
}

# Load the start_action.json and perform a POST to Teams WebHook to notify the channel that the script has been started
jsonfile_start = open('../start_action.json')
datastore_start = json.load(jsonfile_start)
requests.post(config.get('webhook', 'url'), data=json.dumps(datastore_start), proxies=proxyDict)

## kafka_connector_name
kafka_connector_name = Core
kafka_connector_name.check_worker(port=config.get('kafka_connector_name', 'port'), status=config.get('kafka_connector_name', 'status'),
                             action=config.get('kafka_connector_name', 'worker_restart'))
kafka_connector_name.check_task(port=config.get('kafka_connector_name', 'port'),status=config.get('kafka_connector_name', 'status'),
                           action=config.get('kafka_connector_name', 'task_restart'))



# Load the stop_action.json and perform a POST to Teams WebHook to notify the channel that the script has been done
jsonfile_stop = open('../stop_action.json')
datastore_stop = json.load(jsonfile_stop)
requests.post(config.get('webhook', 'url'), data=json.dumps(datastore_stop), proxies=proxyDict)