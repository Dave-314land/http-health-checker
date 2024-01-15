import typer
import requests
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


if __name__ == "__main__":
    typer.run(return_endpoint_status)
