import requests
import configparser
from requests.exceptions import HTTPError
import json

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Set the proxy to Call the Microsoft Teams WebHook
proxyDict = {
        'http': 'http://proxy:8080',
        'https': 'http://proxy:8080'
}

class Core:

    # Function to check worker's status
    # if not running a request.post method will restart the worker
    def check_worker(port, status, action):
        for url in ['http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:',
                    'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:']:
            try:
                response = requests.get((url + port), timeout=5)
                response.raise_for_status()
                # if with break in case of status code == 200 to avoid multiple Kubernetes PODs in cronjobs
                if response.status_code == 200:
                    # GET to REST API to get the status
                    worker_json = requests.get(url + status)
                    # Handle the output as JSON
                    json_get = worker_json.json()
                    # Parsing JSON to get the worker's status
                    elements_worker = json_get['connector']['state']
                    if 'RUNNING' not in elements_worker:
                        # POST to REST API to restart the worker
                        requests.post(url + action)
                        # Building payload for the alerting to Teams
                        payload = {'title': json_get['name'], 'text': 'The Worker has been restarted'}
                        # POST to Microsoft Teams WebHook
                        requests.post(config.get('webhook', 'url'), data=json.dumps(payload), proxies=proxyDict)
                        break
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')

    # Function to check the connector's task status
    # if not running a request.post method will restart the task
    def check_task(port, status, action):
        for url in ['http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:',
                    'http://broker_IP_or_hostname:', 'http://broker_IP_or_hostname:']:
            try:
                response = requests.get((url + port), timeout=5)
                response.raise_for_status()
                # if with break in case of status code == 200 to avoid multiple Kubernetes PODs in cronjobs
                if response.status_code == 200:
                    # GET to REST API to get the status
                    task_json = requests.get(url + status)
                    # Handle the output as JSON
                    json_get = task_json.json()
                    # Parsing JSON to get the whole list of Tasks
                    elements_task = json_get['tasks']
                    for task in elements_task:
                        if "RUNNING" not in task['state']:
                            # getting the Task ID
                            my_id = task.get('id')
                            # POST to REST API to restart the Task ID
                            requests.post(url + action + str(my_id) + '/restart')
                            # Building payload for the alerting to Teams
                            payload = {'title': json_get['name'],
                                       'text': 'Task ID:  ' + str(my_id) + '   Has been restarted'
                                       }
                            # POST to Microsoft Teams WebHook to be notified that the ID Has been restarted
                            requests.post(config.get('webhook', 'url'), data=json.dumps(payload), proxies=proxyDict)
                            break
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')