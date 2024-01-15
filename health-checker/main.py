import time
from datetime import timedelta

import requests
import typer
import yaml


yamlFile = 'urls.yaml'


def get_endpoints_from_file(urlFile):
    with open(urlFile, 'r', encoding='utf-8') as file:
        data = yaml.full_load(file)
        endpoints = []
        for row in data:
            endpoint = {
                'headers': row.get('headers'),
                'method': row.get('method'),
                'name': row.get('name'),
                'url': row.get('url'),
                'body': row.get('body')
            }

            endpoints.append(endpoint)
        return endpoints


def return_endpoint_status():
    endpoints = get_endpoints_from_file(yamlFile)
    for endpoint in endpoints:
        url = endpoint.get('url')
        name = endpoint.get('name')
        response = requests.get(url)
        if response.status_code and response.elapsed < timedelta(microseconds=500000):
            print(f'{name} is UP')
        else:
            print(f'{name} is DOWN')


def run_health_checker():
    i = 0
    while True:
        i += 1
        print(f'Test Cycle {i}')
        return_endpoint_status()
        time.sleep(15)


if __name__ == "__main__":
    typer.run(run_health_checker)
