"""
HTTP Health Checker
A program to check the health of a set of HTTP endpoints fed in from a yaml file
"""
import time
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta
from urllib.parse import urlparse

import requests
import typer
import yaml


ENDPOINTS = []
DOMAINS = {}
TOTAL_AVAILABILITY_COUNT = 0


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
                'body': row.get('body')
            }
            ENDPOINTS.append(endpoint)


def extract_domains():
    """Creates a set of unique domains"""
    endpoints = ENDPOINTS
    domain_set = set()
    for endpoint in endpoints:
        url = endpoint.get('url')
        domain = urlparse(url).netloc
        domain_set.add(domain)
    return domain_set


def sort_domains(the_set):
    """Sorting domains for consistent output"""
    return sorted(the_set)


def transform_domain_set_to_dict():
    """Transforms set into dictionary"""
    domain_set = extract_domains()
    sorted_domains = sort_domains(domain_set)
    for domain in sorted_domains:
        DOMAINS[domain] = 0


def total_availability_counter():
    """Increases count by 1"""
    global TOTAL_AVAILABILITY_COUNT
    TOTAL_AVAILABILITY_COUNT += 1


def calculate_domain_availability():
    """Caculates the availability of the domains"""
    domains = DOMAINS
    for domain, up_count in domains.items():
        #print(domain, up_count)
        domain_availability = round(100 * (up_count/TOTAL_AVAILABILITY_COUNT))
        print(f'{domain} has {domain_availability}% availability percentage and total avail count is {TOTAL_AVAILABILITY_COUNT}')


def build_payload(endpoint):
    """Builds the payload from endpoint data"""
    header_data = endpoint.get('headers')
    body_data = endpoint.get('body')
    payload = {
        'headers': header_data,
        'body': body_data
    }
    return payload


def set_request_structure(endpoint):
    """Sets the request structure for the endpoint response"""
    url = endpoint.get('url')
    method = endpoint.get('method')
    payload = build_payload(endpoint)
    default_get_request = requests.get(url, params=payload, timeout=10)
    http_methods = {
        'GET': requests.get(url, params=payload, timeout=10),
        'POST': requests.post(url, data=payload, timeout=10),
        'PUT': requests.put(url, data=payload, timeout=10),
        'PATCH': requests.patch(url, data=payload, timeout=10),
        'HEAD': requests.head(url, timeout=10)
    }
    response = http_methods.get(method, default_get_request)
    return response


def return_endpoint_status():
    """Returns endpoint status"""
    endpoints = ENDPOINTS
    domains = DOMAINS
    for endpoint in endpoints:
        total_availability_counter()
        response = set_request_structure(endpoint)
        url = endpoint.get('url')
        domain = urlparse(url).netloc
        if response.status_code and response.elapsed < timedelta(microseconds=500000):
            domains[domain] += 1
    calculate_domain_availability()


def run_health_checker():
    """Runs program on a loop"""
    parse_endpoints_from_file()
    transform_domain_set_to_dict()
    i = 0
    while True:
        i += 1
        print(f'Test cycle #{i}')
        return_endpoint_status()
        time.sleep(15)


if __name__ == "__main__":
    typer.run(run_health_checker)
