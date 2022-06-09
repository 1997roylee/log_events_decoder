from .base_decoder import BaseDecoder

class SimpleTransfer(BaseDecoder):
    def __init__(self, log_event):
        super().__init__(log_event)

    def extract_token_id(self):
        if self.is_transfer_method(self.log_event['topics'][0]) and len(self.log_event['topics']) == 4:
            if self.price_hex != None:
                if self.price_hex in self.log_event['data']:
                    return None
                            
            self.token_id =  int(self.log_event['topics'][3], 16)
            self.from_address = self.log_event['topics'][1]
            self.to_address = self.log_event['topics'][2]
            self.token_address = self.log_event['address']    
            return self.token_id
        return None