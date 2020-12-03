import requests
import configparser
from core_stream import Core
import json

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Set the proxy to Call the Microsoft Teams WebHook
proxyDict = {
        'http': 'http://proxy:8080',
        'https': 'http://proxy:8080'
}


kafka_stream_name = Core
kafka_stream_name.streamapp_status(port=config.get('kafka_stream_name', 'port'), api=config.get('kafka_stream_name', 'api'))
kafka_stream_name.stream_lag(port=config.get('kafka_stream_name', 'port'), api=config.get('kafka_stream_name', 'api'))