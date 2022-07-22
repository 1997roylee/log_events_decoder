from .client import Client
import json


class Transaction(object):
    def __init__(self, address=None, client=Client()):
        self.client = client
        self.address = address
        self.has_next = False
        self.data = []
        self.pagination = {}
        self.total_size = 0

    def get_transactions(self, page_number=0):
        transactions = self.client.get_transactions(self.address, page_number)
        self.data = transactions['data']
        self.pagination = self.data.get("pagination")
        self.has_next = self.pagination.get("has_more")
        self.total_size = len(self.data.get("items"))
        return self

    def save(self, id=0):
        name = "{}_{}_{}".format(self.address, id, self.total_size)
        with open("raw_transactions/{}/{}.json".format(self.address, name), "wb") as f:
            f.write(json.dumps(self.data).encode("utf-8"))

    @classmethod
    def create_and_get_transactions(cls, address=None, page_number=0):
        instance = cls(address)
        return instance.get_transactions(page_number)
