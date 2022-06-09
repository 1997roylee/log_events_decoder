from .simple_transfer import SimpleTransfer

WETH_CONTRACT = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'

class SimpleSale(SimpleTransfer):
    def __init__(self, log_events):
        super().__init__(log_events)
        # self.setup()
        
    # def setup(self):
    #     self.extract_sale_price()
    
    def extract_sale_price(self):
        self.price_hex = self.extract_price_hex()
        buyer = self.sale_log_event['topics'][1]
        seller = self.sale_log_event['topics'][2]
        self.currency = "ETH"
        for log_event in self.log_events:
            if self.is_transfer_method(log_event['topics'][0]):
                if len(log_event['topics']) == 3:
                    if self.is_price_hex_in_data(log_event['data']):
                        self.currency = self.extract_currency(buyer, seller, log_event)
                    
    def extract_price_hex(self):
        return self.sale_log_event['data'][-64:]
    
    def is_price_hex_in_data(self, data):
        return self.price_hex in data
    
    def extract_currency(self, buyer, seller, log_event):
        address = log_event['address']
        topic_1 = log_event['topics'][1]
        topic_2 = log_event['topics'][2]
        
        if address == WETH_CONTRACT and topic_1 == buyer and topic_2 == seller:
            return 'WETH'
        elif topic_2 == buyer and topic_1 == seller:
            return 'NONETH-' + address
        else:
            return "ETH"
