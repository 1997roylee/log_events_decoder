# data = "0x00000000000000000000000000000000000000000000000000000000000000007656e0665c6bdc38947d580d2e8c4c19ba8fa4019abb8fef31cfaa1b7645f00d000000000000000000000000000000000000000000000000027f7d0bdb920000"
# price_wei = int("0x" + data[-64:], 16)
# price_eth = price_wei / 10**18
# print(price_wei, price_eth)


from this import d
import numpy as np
from pandas import DataFrame, concat
from lib import TransferDecoder
import requests
import json
# import pandas as pd
API_KEY = "R9KSKMIXSBC666KXD937NYNXNHU36XX2M8"


def get_transaction_receipt(txn):
    url = 'https://api.etherscan.io/api'
    params = {
        'module': 'proxy',
        'action': 'eth_getTransactionReceipt',
        'apikey': API_KEY,
        'txhash': txn
    }
    r = requests.get(url, params=params)
    json_data = json.loads(r.text)["result"]
    return json_data


# print(get_transaction_receipt("0xc4799a1224ded0716b62e6d4bed621c15d14966219c45a8bec20c60a74e94298"))

WETH_CONTRACT = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
OPENSEA_CONTRACT = '0x7be8076f4ea4a4ad08075c2508e481d6c946d12b'
TRANSFER_METHOD = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'


log_events = []


def determine_currency(txn):
    # mentioned earlier function
    transaction_receipt = get_transaction_receipt(txn)
    global log_events
    log_events = log_events + transaction_receipt['logs']


aa = [
    # "0x0a9940e52075ec69cddd7670ceaf2605112f04afca2c9c23d747e699652cfd02"
    # "0x372f0c02029f397d1d4f6e79add7682fd45f25595b92ef954226a3940e16abb1",
    # "0x5c306753cf7facd1b1d17183fdd0c666cd442feb0fdbcbaf99b3f1ecb875fa03",
    # "0xfda0746691b998a06171d7c418f94280c7dffbb244bcabedd5f5aef3afbf20f6",
    # "0x39ed208ca02eaa81e85c7bdd86f7df98ad4de4a748cc69d6b2749e3a0fe739cd",
    # "0x8127fa64e9a8ab7443364d4d93e4a5e2e52fdf440843e5127c09c40674de3ef8",
    # "0x5ab972ff08e2ce03f4178a5e0375f8a3b3f0cae00d57c1fb8b8a04fd9e42280c",
    # "0x37a69a1ed42fe110ccc9e890bde73b8b0b523923196dff13bdb31ba753eb4a18",
    # "0x2f6140d84cb78662cb5acf97a118328f558c5b854aa3aa4be6c4bf3ef7c170e0",
    # "0x14bd459f3c555049f26c378e7ea7a3edaf895b416462d83a06775ad1873d64cc"
    # "0x757cfe2ca2354132c3ab842c53fe00ff0be5c8e67d8808c41f5b98af7e319331",
    # "0x30b1201c73f2c737378d7af00b13a5870d47a141a33f277192c726ce45e28a95",
    "0xb624c8c51422dc1c1f08342341a3fbc8e06b5a471bc1450f2bda82bc141d1f6d",
    "0x9058ad0eee3a29b8f407216a6c36d86ab6506876f663e1bcf9333176517be28a",
    "0x47c6897e3de42585403e8ecd198c4211be05375f8cdc1fa636af6a5cab436611",
    "0x58f8619ba4854307f053c318bb5f973c23c68cfbcc34d2766a0c994359ffb48c"
]
for a in aa:
    determine_currency(a)

logs_df = DataFrame(log_events, columns=[
                    'address', 'topics', 'data', 'blockNumber', 'transactionHash', 'blockHash', 'logIndex'])
# print(log_events_df.query('topics[0] == @TRANSFER_METHOD'))


event_signature_hash = [
    '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
]

transfers_df = logs_df.loc[logs_df["topics"].str.get(
    0).isin(event_signature_hash)]


sales_df = logs_df.loc[logs_df["topics"].str.get(
    0).isin(['0xc4109843e0b7d514e4c093114b863f8e7d8d9a458c372cd51bfe526b588006c9'])]


sales_df['maker'] = sales_df['topics'].str.get(1)
sales_df['taker'] = sales_df['topics'].str.get(2)
sales_df['revert'] = False
sales_df['price'] = sales_df['data'].apply(
    lambda x: int(x[-64:], 16))

sales_df = sales_df[['maker', 'taker', 'price', 'revert', 'transactionHash']]
revert_sales_df = sales_df.copy()
revert_sales_df['revert'] = True
taker = revert_sales_df['taker']
maker = revert_sales_df['maker']
revert_sales_df['maker'] = taker
revert_sales_df['taker'] = maker

all_sales_df = concat([sales_df, revert_sales_df])

nft_transfers_df = transfers_df.loc[transfers_df["topics"].str.len() == 4]
nft_transfers_df['from'] = transfers_df['topics'].str.get(1)
nft_transfers_df['to'] = transfers_df['topics'].str.get(2)
nft_transfers_df['tokenId'] = transfers_df['topics'].str.get(3)

non_nft_transfers_df = transfers_df.loc[transfers_df["topics"].str.len() == 3]
non_nft_transfers_df['sender'] = transfers_df['topics'].str.get(1)
non_nft_transfers_df['receiver'] = transfers_df['topics'].str.get(2)
non_nft_transfers_df['currency'] = non_nft_transfers_df['address']
non_nft_transfers_df = non_nft_transfers_df[[
    'sender', 'receiver', 'currency', 'transactionHash']]


nft_transfers_df = nft_transfers_df.merge(non_nft_transfers_df, left_on=[
                                          'from', 'to', 'transactionHash'], right_on=['receiver', 'sender', 'transactionHash'], how='left')


nft_transfers_df = nft_transfers_df.merge(
    all_sales_df, left_on=['from', 'to', 'transactionHash'], right_on=['maker', 'taker', 'transactionHash'], how='left')

for index, row in nft_transfers_df.iterrows():
    decoder = TransferDecoder(row)
    print("From %s to %s, token_id: %s, price: %s" % (decoder.from_address,
          decoder.to_address, str(decoder.token_id), str(decoder.price)))
