from pandas import DataFrame

EVENT_SIGNATURE_HASH = [
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
]

SALE_SIGNATURE_HASH = [
    "0xc4109843e0b7d514e4c093114b863f8e7d8d9a458c372cd51bfe526b588006c9"
]

class DataFrameDecoder():
    def __init__(self, df):
        self.df = df
        
    def transfers(self):
        return self.df.loc[self.df["action"] == "Transfer"]
    
    def sales(self):
        sales_df = self.df.loc[self.df["action"] == "Sale"]
        sales_df['maker'] = sales_df['topics'].str.get(1)
        sales_df['taker'] = sales_df['topics'].str.get(2)
        sales_df['revert'] = False
        sales_df['price'] = sales_df['raw_log_data'].apply(
            lambda x: int(x[-64:], 16))
        return sales_df[['maker', 'taker', 'price', 'revert', 'tx_hash']]

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

    @property
    def topics(self):
        return self.raw_log_topics

    @property
    def action(self):
        if self.topics[0] in EVENT_SIGNATURE_HASH:
            return "Transfer"
        elif self.topics[0] in SALE_SIGNATURE_HASH:
            return "Sale"

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
            "tx_hash": self.tx_hash,
        }

    @classmethod
    def to_data_frame(cls, log_events):
        rows = list(map(lambda log_event: log_event.to_data_frame_row(), log_events))
        return DataFrameDecoder(DataFrame(rows))