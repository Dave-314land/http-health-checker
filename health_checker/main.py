"""
HTTP Health Checker
A program to check the health of a set of HTTP endpoints fed in from a yaml file
"""

import time
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta

import requests
import typer
import yaml


def get_file():
    """Prompts user to select a file with a file dialog"""
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename()
    return file


def parse_endpoints_from_file(url_file):
    """Creates endpoint entries from passed-in file"""
    with open(url_file, 'r', encoding='utf-8') as file:
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
    """Returns endpoint status"""
    url_file = get_file()
    endpoints = parse_endpoints_from_file(url_file)
    for endpoint in endpoints:
        url = endpoint.get('url')
        name = endpoint.get('name')
        response = requests.get(url, timeout=10)
        if response.status_code and response.elapsed < timedelta(microseconds=500000):
            print(f'{name} is UP')
        else:
            print(f'{name} is DOWN')


def run_health_checker():
    """Runs program on a loop"""
    i = 0
    while True:
        i += 1
        print(f'Test Cycle {i}')
        return_endpoint_status()
        time.sleep(15)


if __name__ == "__main__":
    typer.run(run_health_checker)
