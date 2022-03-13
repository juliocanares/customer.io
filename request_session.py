import requests
from urllib3 import Retry


def get_request_session():
    session = requests.Session()

    retries = Retry(total=3, status_forcelist=(500, 501, 502))

    adapter = requests.adapters.HTTPAdapter(max_retries=retries)

    session.mount('http://', adapter)

    session.mount('https://', adapter)

    return session