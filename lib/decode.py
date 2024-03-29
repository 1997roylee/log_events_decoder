# from .simple_sale import SimpleSale
# from .simple_transfer import SimpleTransfer
# from .base_decoder import BaseDecoder
import pandas as pd
# import numpy as np
WETH_CONTRACT = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
APE_CONTRACT = "0x4d224452801aced8b2f0aebe155379bb5d594381"
USDC_CONTRACT = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'

class TransferDecoder():
    def __init__(self, transfer):
        self._decode(transfer)

    def to_json(self):
        return {
            "contract_address": self.contract_address,
            "transaction_hash": self.transaction_hash,
            "block_number": self.block_number,
            "action": self.action,
            "taker": self.taker,
            "maker": self.maker,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "currency": self.currency,
            "price": self.price,
            "token_id": self.token_id,
            "block_signed_at": self.block_signed_at,
            "log_offset": self.log_offset,
        }

    def _clean(self, value):
        if pd.isnull(value):
            return ""

        return value

    def _decode(self, transfer):
        self.contract_address = self._clean(transfer.get('sender_address'))
        self.transaction_hash = self._clean(transfer.get('tx_hash'))
        self.block_number = self._clean(transfer.get('block_height'))
        self.taker = self._clean(transfer.get('taker'))
        self.maker = self._clean(transfer.get('maker'))
        self.action = self._clean(transfer.get('action'))
        self.block_signed_at = self._clean(transfer.get('block_signed_at'))
        self.from_address = self._clean(transfer.get('from')[-40:])
        self.to_address = self._clean(transfer.get('to')[-40:])
        self.currency = self._clean(self._decode_currency(transfer.get('currency')))
        self.price = self._clean(self._decode_price(transfer.get('price'), self.currency))
        self.token_id = self._clean(int(transfer.get('tokenId'), base=16))
        self.log_offset = self._clean(transfer.get('log_offset'))

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
