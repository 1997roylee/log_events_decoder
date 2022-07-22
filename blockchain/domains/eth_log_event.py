class EthLogEvent(object):
    def __init__(self, log_event):
        self.block_height = log_event.get("block_height")
        self.tx_offset = log_event.get("tx_offset")
        self.log_offset = log_event.get("log_offset")
        self.transaction_hash = log_event.get("tx_hash")
        self.raw_log_topics = log_event.get("raw_log_topics")
        self.sender_name = log_event.get("sender_name")
        # self.sender_contract_ticker_symbol = log_event.get(
        #     "sender_contract_ticker_symbol")
        self.sender_address = log_event.get("sender_address")
        self.sender_address_label = log_event.get("sender_address_label")
        self.raw_log_data = log_event.get("raw_log_data")
        self.decoded = log_event.get("decoded")
        self.block_signed_at = log_event.get("block_signed_at")
        
    @property
    def topics(self):
        return self.raw_log_topics

    @property
    def maker(self):
        return self.topics[1]

    @property
    def taker(self):
        return self.topics[2]

    @property
    def price(self):
        return self.raw_log_data.apply(lambda x: int(x[-64:], 16))
    
    def to_json(self):
        return {
            "block_height": self.block_height,
            "log_offset": self.log_offset,
            "transaction_hash": self.transaction_hash,
            "sender_address": self.sender_address,
            "block_signed_at": self.block_signed_at,
            "raw_log_data": self.raw_log_data,
            "topics": self.topics,
        }