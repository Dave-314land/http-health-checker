import typer
import requests
import time
from datetime import timedelta


urls = [
    'https://fetch.com/',
    'https://fetch.com/careers',
    'https://fetchrewards.com/'
]


def return_endpoint_status():
    for url in urls:
        response = requests.get(url)
        if response.status_code and response.elapsed < timedelta(microseconds=500000):
            print('UP')
        else:
            print('DOWN')


def run_health_checker():
    i = 0
    while True:
        i += 1
        print(f'Test Cycle {i}')
        return_endpoint_status()
        time.sleep(15)


if __name__ == "__main__":
    typer.run(run_health_checker)
