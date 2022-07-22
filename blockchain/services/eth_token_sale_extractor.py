from pandas import DataFrame, concat
from blockchain.domains.eth_token_sale import EthTokenSale
# from blockchain.domains.eth_token_sale import EthTokenSale
from blockchain.services.opensea_sale_extractor import OpenseaSaleExtractor
from blockchain.services.opensea_seaport_sale_extractor import OpenseaSeaportSaleExtractor

TRANSFER_EVENT_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


class EthTokenSaleExtractor:
    def extract_token_non_transfer_from_log_event(self, log_event):
        topics = log_event.topics
        if len(topics) == 3 and topics[0].casefold() == TRANSFER_EVENT_TOPIC:
            eth_token_sale = EthTokenSale()
            eth_token_sale.sender = topics[1]
            eth_token_sale.receiver = topics[2]
            eth_token_sale.currency = log_event.sender_address
            eth_token_sale.transaction_hash = log_event.transaction_hash
            return eth_token_sale
        else:
            return None

    def extract_token_sales_from_log_events(self, eth_log_event_list, eth_token_non_transfer_list):
        df = DataFrame(eth_log_event_list)
        non_transfer_df = DataFrame(eth_token_non_transfer_list)
        opensea_v1_sale_df = df[df["sender_address"] ==
                                "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"]  # OpenSea v1
        
        opensea_v2_sale_df = df[df["sender_address"] ==
                                "0x7f268357a8c2552623316e2562d90e642bb538e5"]  # OpenSea v2
        
        opensea_v11_sale_df = df[df["sender_address"] ==
                                 "0x00000000006c3852cbef3e08e8df289169ede581"]  # OpenSea v1.1
        
        # df[df["sender_address"] == "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"] # LooksRare
        # df[df["sender_address"] == "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"] # X2Y2 Exchange
        sales_df1 = OpenseaSaleExtractor(opensea_v1_sale_df).get_sales()
        sales_df1['market_place'] = "OpenSea v1"
        sales_df2 = OpenseaSaleExtractor(opensea_v2_sale_df).get_sales()
        sales_df2['market_place'] = "OpenSea v2"
        sales_df3 = OpenseaSeaportSaleExtractor(
            opensea_v11_sale_df).get_sales()
        sales_df3['market_place'] = "OpenSea v1.1"

        all_sales_df = concat([sales_df1, sales_df2, sales_df3])
        all_sales_df = all_sales_df.merge(non_transfer_df, left_on=['maker', 'taker', 'transaction_hash'], right_on=[
                                          'receiver', 'sender', 'transaction_hash'], how='left')
        all_sales_df.to_csv("a.csv")
        return all_sales_df[['maker', 'taker', 'price', 'transaction_hash', 'sender', 'receiver', 'currency', 'market_place']]
