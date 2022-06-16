# from .simple_sale import SimpleSale
# from .simple_transfer import SimpleTransfer
# from .base_decoder import BaseDecoder
import pandas as pd
WETH_CONTRACT = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
APE_CONTRACT = "0x4d224452801aced8b2f0aebe155379bb5d594381"
USDC_CONTRACT = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'

class TransferDecoder():
    def __init__(self, transfer):
        self._decode(transfer)

    def _decode(self, transfer):
        self.contract_address = transfer.get('sender_address')
        self.transaction_hash = transfer.get('tx_hash')
        self.block_number = transfer.get('blockNumber')
        self.block_hash = transfer.get('blockHash')
        self.taker = transfer.get('taker')
        self.maker = transfer.get('maker')
        self.from_address = transfer.get('from')[-40:]
        self.to_address = transfer.get('to')[-40:]
        self.currency = self._decode_currency(transfer.get('currency'))
        self.price = self._decode_price(transfer.get('price'), self.currency)
        self.token_id = int(transfer.get('tokenId'), base=16)

    def _decode_price(self, price, currency):
        currency_unit_list = {
            "ETH": 10 ** 18,
            "WETH": 10 ** 18,
            "APE": 10 ** 18,
            "USDC": 10 ** 6
        }
        if currency_unit_list.get(currency, None) == None:
            return price
        else:
            return price / currency_unit_list.get(currency)

    def _decode_currency(self, currency):
        if currency == None or pd.isnull(currency):
            return "ETH"
        elif currency == WETH_CONTRACT:
            return 'WETH'
        elif currency == APE_CONTRACT:
            return 'APE'
        elif currency == USDC_CONTRACT:
            return 'USDC'
        else:
            return 'NONETH-' + str(currency)
