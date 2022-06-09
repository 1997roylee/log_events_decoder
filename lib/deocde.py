# from .simple_sale import SimpleSale
# from .simple_transfer import SimpleTransfer
# from .base_decoder import BaseDecoder
import pandas as pd
WETH_CONTRACT = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'


class TransferDecoder():
    def __init__(self, transfer):
        self._decode(transfer)

    def _decode(self, transfer):
        self.contract_address = transfer.get('address')
        self.transaction_hash = transfer.get('transactionHash')
        self.block_number = transfer.get('blockNumber')
        self.block_hash = transfer.get('blockHash')
        self.taker = transfer.get('taker')
        self.maker = transfer.get('maker')
        self.from_address = transfer.get('from')[-40:]
        self.to_address = transfer.get('to')[-40:]
        self.currency = self._decode_currency(transfer.get('currency'))
        self.price = transfer.get('price')
        self.token_id = int(transfer.get('tokenId'), base=16)

    def _decode_currency(self, currency):
        if currency == None or pd.isnull(currency):
            return "ETH"
        elif currency == WETH_CONTRACT:
            return 'WETH'
        else:
            return 'NONETH-' + str(currency)
