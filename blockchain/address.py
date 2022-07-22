import glob
import re
from .transaction import Transaction


class Address(object):
    def __init__(self, address=None):
        self.address = address
        self.transaction = Transaction

    def last_transaction_page_id(self):
        files = glob.glob("raw_transactions/{}/*.json".format(self.address))
        id_list = []
        for file in files:
            id = re.search("{}_(.*)_".format(self.address), file)
            if (id):
                # print(id[1])
                id_list.append(int(id[1]))

        if len(id_list) == 0:
            return 0
        
        return max(id_list) + 1
