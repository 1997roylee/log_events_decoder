from .api_requestor import ApiRequestor
from .constants import API_ENDPOINT, API_VERSION, API_KEY


class Client(object):
    def __init__(self, base_url=API_ENDPOINT, api_version=API_VERSION):
        self.base_url = base_url
        self.api_version = api_version
        self.api_url = self.base_url + "/" + self.api_version
        self.api_requestor = ApiRequestor(self.api_url)

    def get_transactions(self, address, page_number=0, page_size=500):
        path = "/1/address/{}/transactions_v2/".format(address)
        return self.api_requestor.get(path, params={
            "quote-currency": "USD",
            "format": "json",
            "block-signed-at-asc": True,
            "no-logs": False,
            "page-size": page_size,
            'page-number': page_number,
            "key": API_KEY,
        })
