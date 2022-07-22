from pandas import DataFrame, concat

EVENT_SIGNATURE_HASH = [
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
]


SALE_SIGNATURE_HASH_DICT = {
    "0xc4109843e0b7d514e4c093114b863f8e7d8d9a458c372cd51bfe526b588006c9": "OrdersMatchedSig",
    "0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31": "0xfb0f3ee1" # OpenSea: Seaport 1.1
}

from .extract_sales import ExtractOpenseaSales, ExtractOpenseaSeaportSales

class DataFrameDecoder():
    def __init__(self, df):
        self.df = df
        af = ExtractOpenseaSales(df.loc[df["action"] == "OrdersMatchedSig"]).get_sales()
        bf = ExtractOpenseaSeaportSales(self.df.loc[self.df["action"] == "0xfb0f3ee1"]).get_sales()
        self.sales_df = concat([i for i in [af, bf] if not i.empty])
        # self.transfers_df = self.df.loc[self.df["action"] == "Transfer"]
        
        
    def nft_transfers(self):
        transfers_df = self.transfers_df
        nft_transfers_df = transfers_df.loc[transfers_df["topics"].str.len() == 4]
        nft_transfers_df['from'] = transfers_df['topics'].str.get(1)
        nft_transfers_df['to'] = transfers_df['topics'].str.get(2)
        nft_transfers_df['tokenId'] = transfers_df['topics'].str.get(3)
        nft_transfers_df.loc[nft_transfers_df['from'] == "0x0000000000000000000000000000000000000000000000000000000000000000", 'action'] = "Minted"
        nft_transfers_df = nft_transfers_df.merge(self.non_nft_transfers(), left_on=[
                                            'from', 'to', 'tx_hash'], right_on=['receiver', 'sender', 'tx_hash'], how='left')
        nft_transfers_df = nft_transfers_df.merge(self.sales_df, left_on=['from', 'to', 'tx_hash'], right_on=['maker', 'taker', 'tx_hash'], how='left')
        
        return nft_transfers_df

    def non_nft_transfers(self):
        transfers_df = self.transfers_df 
        non_nft_transfers_df = transfers_df.loc[transfers_df["topics"].str.len() == 3]
        non_nft_transfers_df['sender'] = transfers_df['topics'].str.get(1)
        non_nft_transfers_df['receiver'] = transfers_df['topics'].str.get(2)
        non_nft_transfers_df['currency'] = non_nft_transfers_df['sender_address']
        return non_nft_transfers_df[[
            'sender', 'receiver', 'currency', 'tx_hash']]

class LogEventDecoder():
    def __init__(self, log_event):
        self.block_height = log_event.get("block_height")
        self.tx_offset = log_event.get("tx_offset")
        self.log_offset = log_event.get("log_offset")
        self.tx_hash = log_event.get("tx_hash")
        self.raw_log_topics = log_event.get("raw_log_topics")
        self.sender_name = log_event.get("sender_name")
        self.sender_contract_ticker_symbol = log_event.get(
            "sender_contract_ticker_symbol")
        self.sender_address = log_event.get("sender_address")
        self.sender_address_label = log_event.get("sender_address_label")
        self.sender_logo_url = log_event.get("sender_logo_url")
        self.raw_log_data = log_event.get("raw_log_data")
        self.decoded = log_event.get("decoded")
        self.block_signed_at = log_event.get("block_signed_at")

    @property
    def topics(self):
        return self.raw_log_topics

    @property
    def action(self):
        first_topic = self.topics[0]
        if first_topic in EVENT_SIGNATURE_HASH:
            return "Transfer"
        else:
            return SALE_SIGNATURE_HASH_DICT.get(first_topic)

    @property
    def maker(self):
        return self.topics[1]

    @property
    def taker(self):
        return self.topics[2]

    @property
    def price(self):
        return self.raw_log_data.apply(lambda x: int(x[-64:], 16))
    
    def to_data_frame_row(self):
        return {
            "topics": self.topics,
            "sender_address": self.sender_address,
            "action": self.action,
            "raw_log_data": self.raw_log_data,
            "block_height": self.block_height,
            "block_signed_at": self.block_signed_at,
            "tx_hash": self.tx_hash,
            "log_offset": self.log_offset,
        }

    @classmethod
    def to_data_frame(cls, log_events):
        rows = list(map(lambda log_event: log_event.to_data_frame_row(), log_events))
        return DataFrameDecoder(DataFrame(rows))