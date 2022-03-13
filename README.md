### Intro

This project reads a large json file of customers and start to stream it for upsert using the customer.io api.

### Features

- Readable stream
- JSON stream parser
- Queue for parallelism
- Transform keys
- Async requests
- Retries

### Run

- Install depedencies `python3 -m pip install -r requirements.txt`
- Set a key `credentials` in configuration.json like:

```json
{
  "credentials": {
    "siteId": "abc",
    "apiKey": "xyz"
  }
}
```

or use a .env file, touch `.env` and set the values:

```sh
CUSTOMER_IO_SITE_ID=abc
CUSTOMER_IO_API_KEY=xyz
```

configuration values are preferred.

- Run the synchronizer: `python3 sync.py`
