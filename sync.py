import sys
import grequests
import json
import requests
from queue import Queue
import json_stream
from urllib3 import Retry

num_of_args = len(sys.argv)

config_filename = sys.argv[1] if num_of_args > 1 else 'configuration.json'
data_filename = sys.argv[2] if num_of_args > 2 else 'data.json'

config_file = json.loads(open(config_filename).read())


def get_request_session():
    session = requests.Session()

    retries = Retry(total=3, status_forcelist=(500, 501, 502))

    adapter = requests.adapters.HTTPAdapter(max_retries=retries)

    session.mount('http://', adapter)

    session.mount('https://', adapter)

    return session


request_session = get_request_session()


endpoint = 'https://track.customer.io/api/v1/customers/{identifier}'


def create_customer(customer):
    url = endpoint.format(identifier=customer['id'])

    params = {
        "auth": (config_file['credentials']['siteId'],
                 config_file['credentials']['apiKey']),
        "json": customer,
        "session": request_session,
        "timeout": 3
    }

    return grequests.put(url, **params)


batch = Queue(config_file['parallelism'])


def create_customers(batch):
    batch_size = batch.qsize()

    print('upserting {size} new customers'.format(size=batch_size))

    customers_to_create = []

    for _ in range(batch_size):
        customer = dict(batch.get())

        for pair in config_file['mappings']:
            if pair['from'] in customer:
                customer[pair['to']] = customer[pair['from']]
                customer.pop(pair['from'], None)

        customers_to_create.append(create_customer(customer))

    grequests.map(customers_to_create)


def main():
    with open(data_filename, mode='r', encoding='utf8') as file:
        items = json_stream.load(file)

        for item in items.persistent():
            batch.put(item)
            if batch.full():
                create_customers(batch)


main()
