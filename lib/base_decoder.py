APE_TRANSFER_METHOD = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
# Opensea
OPENSEA_CONTRACT = "0x7f268357a8c2552623316e2562d90e642bb538e5"
ORDERS_MATCHED_METHOD = "0xc4109843e0b7d514e4c093114b863f8e7d8d9a458c372cd51bfe526b588006c9"


class BaseDecoder(object):
    def __init__(self, log_event=None):
        self.log_event = log_event
        self.currency = None
        self.token_id = None
        self.price_hex = None
        # self.sale_log_event = None
        self.action = None
        self.token_address = None
        self.from_address = None
        self.to_address = None
        # self.setup();

    # def setup(self):
    #     self.sale_log_event = self.find_sale_log_event()
    #     self.sale_log_event = self.sale_log_event[0] if len(
    #         self.sale_log_event) > 0 else None

    def is_transfer_method(self, topic):
        return topic == APE_TRANSFER_METHOD

    def is_sale_method(self, topic):
        return topic == ORDERS_MATCHED_METHOD

    def is_sale_action(self):
        return self.sale_log_event != None

    # def find_sale_log_event(self):
    #     return list(filter(lambda log_event: self.is_sale_method(log_event['topics'][0]), self.log_events))
                    
    @property
    def price(self):
        if self.price_hex != None:
            return int(self.price_hex, 16) / 10**18