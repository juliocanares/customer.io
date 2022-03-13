from dotenv import load_dotenv
import grequests
import json
from queue import Queue
import json_stream
from credentials import get_connections_credentials
from request_session import get_request_session
from arguments import read_arguments
from map_attributes import map_attributes

load_dotenv()

config_filename, data_filename = read_arguments()

config_file = json.loads(open(config_filename).read())

siteId, apiKey = get_connections_credentials(config_file)

queue = Queue(config_file['parallelism'])

request_session = get_request_session()

def create_async_request(customer):
    endpoint = 'https://track.customer.io/api/v1/customers/{identifier}'

    url = endpoint.format(identifier=customer['id'])

    params = {
        "auth": (siteId, apiKey),
        "json": customer,
        "session": request_session,
        "timeout": 3
    }

    return grequests.put(url, **params)

def create_customers(queue):
    queue_size = queue.qsize()

    print('upserting {size} new customers'.format(size=queue_size))

    customers_to_create = []

    for _ in range(queue_size):
        customer = dict(queue.get())

        for pair in config_file['mappings']:
            map_attributes(pair, customer)

        customers_to_create.append(create_async_request(customer))

    grequests.map(customers_to_create)


def main():
    with open(data_filename, mode='r', encoding='utf8') as file:
        items = json_stream.load(file)

        for item in items.persistent():
            queue.put(item)
            if queue.full():
                create_customers(queue)


main()
