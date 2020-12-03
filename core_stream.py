import requests
import configparser
from requests.exceptions import HTTPError
import datetime
import json


# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

proxyDict = {
        'http': 'http://proxy:8080',
        'https': 'http://proxy:8080'
}

class Core:

    def streamapp_status(port, api):
        for url in ['http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:',
                    'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:']:
            # Exception Handling
            try:
                response = requests.get((url + api), timeout=5)
                response.raise_for_status()
                if response.status_code == 200:
                    stream_json = requests.get(url + api)
                    json_get = stream_json.json()
                    stream_status = json_get['status']['status']
                    stream_status_topic = json_get['status']['maxlag']['status']
                    if 'OK' not in stream_status:
                        teams = open("../strem_ko.json")
                        streamKo = teams.read()
                        consumer_grp = (json_get['status']['group'])
                        my_payload = streamKo.replace('app', consumer_grp)
                        requests.post(config.get('webhook', 'url'), data=my_payload, proxies=proxyDict, timeout=6)
                    if 'OK' not in stream_status_topic:
                        # Collect all the metrics to build alerting message with details
                        start_offset = (json_get['status']['maxlag']['start']['offset'])
                        start_tsp = (json_get['status']['maxlag']['start']['timestamp'])
                        end_offset = (json_get['status']['maxlag']['end']['offset'])
                        end_tsp = (json_get['status']['maxlag']['end']['timestamp'])
                        consumer_grp = (json_get['status']['group'])
                        topic = (json_get['status']['maxlag']['topic'])
                        # Epoch Timestamp / 1000 to avoid "year out of range" exception
                        dt_start = datetime.datetime.fromtimestamp(start_tsp / 1000)
                        dt_end = datetime.datetime.fromtimestamp(end_tsp / 1000)
                        # Load custom json for Teams channel
                        teams = open('../topic_ko.json')
                        topicKo = teams.read()
                        # Building payload replacing some value
                        my_payload = topicKo.replace('app', consumer_grp).replace('start_offset', str(start_offset)) \
                            .replace('start_timestamp', str(dt_start)).replace('end_offset', str(end_offset)) \
                            .replace('end_timestamp', str(dt_end)).replace('topic_name', topic)
                        # Calling Teams WebHook
                        requests.post(config.get('webhook', 'url'), data=my_payload, proxies=proxyDict, timeout=6)
                        break
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')


    def stream_lag(port, api):
        for url in ['http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:',
                    'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:']:
            # Exception Handling
            try:
                response = requests.get((url + api), timeout=5)
                response.raise_for_status()
                if response.status_code == 200:
                    # Call Burrow API
                    stream_json = requests.get(url + api)
                    # Transform in JSON output
                    json_get = stream_json.json()
                    # Collect only metrics needed for check
                    stream_lag = json_get['status']['maxlag']['current_lag']
                    if stream_lag >= 5500:
                        # Collect metrics neeeded to reporting
                        consumer_grp = json_get['status']['group']
                        start_offset = json_get['status']['maxlag']['start']['offset']
                        end_offset = json_get['status']['maxlag']['end']['offset']
                        topic = json_get['status']['maxlag']['topic']
                        # Open teh custom json to inject payload
                        teams = open('../stream_lag.json')
                        lag_exceed = teams.read()
                        # Building payload message
                        my_payload = lag_exceed.replace('app', consumer_grp).replace('start_offset', str(start_offset)) \
                            .replace('end_offset', str(end_offset)).replace('topic', topic)
                        requests.post(config.get('webhook', 'url'), data=my_payload, proxies=proxyDict, timeout=6)
                        break
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')