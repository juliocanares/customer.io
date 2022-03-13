
import os


def get_connections_credentials(config):
    siteId = os.getenv('CUSTOMER_IO_SITE_ID')
    apiKey = os.getenv('CUSTOMER_IO_API_KEY')

    if 'credentials' in config:
        siteId = config['credentials']['siteId']
        apiKey = config['credentials']['apiKey']
    
    return (siteId, apiKey)
