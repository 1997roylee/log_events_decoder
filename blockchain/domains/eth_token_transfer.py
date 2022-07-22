from blockchain.utils import format_address

MINTED_ADDRESS = "0x0000000000000000000000000000000000000000000000000000000000000000"


class EthTokenTransfer(object):
    def __init__(self, data=dict()):
        self.token_address = data.get("token_address", None)
        self.transaction_hash = data.get("transaction_hash", None)
        self.log_index = data.get("log_index", None)
        self.block_height = data.get("block_height", None)
        self.block_signed_at = data.get("block_signed_at", None)
        self._from_address = data.get("from_address", None)
        self._to_address = data.get("to_address", None)
        self._token_id = data.get("token_id", None)
        self.action = "Transfer" if self._from_address != MINTED_ADDRESS else "Minted"

    @property
    def from_address(self):
        return format_address(self._from_address)

    @property
    def token_id(self):
        return int(self._token_id, base=16)

    @property
    def to_address(self):
        return format_address(self._to_address)

    @token_id.setter
    def token_id(self, value):
        self._token_id = value

    @from_address.setter
    def from_address(self, address):
        self._from_address = address
        self.action = "Transfer" if address != MINTED_ADDRESS else "Minted"

    @to_address.setter
    def to_address(self, address):
        self._to_address = address

    def to_json(self):
        return {
            "token_address": self.token_address,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "token_id": self.token_id,
            "transaction_hash": self.transaction_hash,
            "log_index": self.log_index,
            "block_height": self.block_height,
            "action": self.action,
            "block_signed_at": self.block_signed_at,
        }
