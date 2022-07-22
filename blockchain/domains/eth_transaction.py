from blockchain.domains.eth_log_event import EthLogEvent

class EthTransaction(object):
    def __init__(self, transaction):
        self.from_address = transaction.get("from_address")
        self.to_address = transaction.get("to_address")
        self.value = transaction.get("value")
        self.value_quote = transaction.get("value_quote")
        self.tx_offset = transaction.get("tx_offset")
        self.tx_hash = transaction.get("tx_hash")
        self.block_height = transaction.get("block_height")
        self.successful = transaction.get("successful")
        self.block_signed_at = transaction.get("block_signed_at")
        self.log_events = list(map(lambda log_event: EthLogEvent(
            log_event), transaction.get("log_events")))