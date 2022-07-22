from blockchain.utils import format_address

class EthTokenSale(object):
    def __init__(self):
        self.sender = None
        self.receiver = None
        self.currency = None
        self.market_place = None
        self.transaction_hash = None
        
    def to_json(self):
        return {
            "sender": format_address(self.sender),
            "receiver": format_address(self.receiver),
            "currency": self.currency,
            "transaction_hash": self.transaction_hash,
        }