from blockchain.domains.eth_token_transfer import EthTokenTransfer
from pandas import DataFrame

TRANSFER_EVENT_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

class EthTokenTransferExtractor(object):
    def extract_token_transfer_from_log_event(self, log_event):
        topics = log_event.topics
        
        if topics[0].casefold() == TRANSFER_EVENT_TOPIC:
            if len(topics) == 4:
                from_address = topics[1]
                to_address = topics[2]
                token_id = topics[3]
                eth_token_transfer = EthTokenTransfer()
                eth_token_transfer.token_address = log_event.sender_address
                eth_token_transfer.from_address = from_address
                eth_token_transfer.to_address = to_address
                eth_token_transfer.token_id = token_id
                eth_token_transfer.block_height = log_event.block_height
                eth_token_transfer.transaction_hash = log_event.transaction_hash
                eth_token_transfer.log_index = log_event.log_offset
                eth_token_transfer.block_signed_at = log_event.block_signed_at
                return eth_token_transfer

        return None

    def reconnect_transfer_relationship(self, eth_token_transfer_list):
        df = DataFrame(eth_token_transfer_list)
        return df
        