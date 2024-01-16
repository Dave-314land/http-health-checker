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


ENDPOINTS = []


def get_file():
    """Prompts user to select a file with a file dialog"""
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename()
    return file


def parse_endpoints_from_file():
    """Creates endpoint entries from passed-in file"""
    yaml_file = get_file()
    with open(yaml_file, 'r', encoding='utf-8') as file:
        data = yaml.full_load(file)
        for row in data:
            endpoint = {
                'headers': row.get('headers'),
                'method': row.get('method'),
                'name': row.get('name'),
                'url': row.get('url'),
                'body': row.get('body'),
                'up_availability_count': 0,
                'total_availability_count': 0
            }
            ENDPOINTS.append(endpoint)


def return_endpoint_status():
    """Returns endpoint status"""
    endpoints = ENDPOINTS
    for endpoint in endpoints:
        endpoint['total_availability_count'] += 1
        total = endpoint.get('total_availability_count')
        url = endpoint.get('url')
        name = endpoint.get('name')
        response = requests.get(url, timeout=10)
        if response.status_code and response.elapsed < timedelta(microseconds=500000):
            endpoint['up_availability_count'] += 1
            up = endpoint.get('up_availability_count')
            availability = round(100 * (up/total))
            print(f'{name} has {availability}% availability percentage')
        else:
            up = endpoint.get('up_availability_count')
            availability = round(100 * (up/total))
            print(f'{name} has {availability}% availability percentage')


def run_health_checker():
    """Runs program on a loop"""
    parse_endpoints_from_file()
    i = 0
    while True:
        i += 1
        print(f'Test cycle #{i}')
        return_endpoint_status()
        time.sleep(15)


if __name__ == "__main__":
    typer.run(run_health_checker)
