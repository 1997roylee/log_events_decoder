from pandas import DataFrame, concat
from .decode import TransferDecoder

COLUMNS = ['address', 'topics', 'data', 'blockNumber', 'transactionHash', 'blockHash', 'logIndex']

EVENT_SIGNATURE_HASH = [
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
]

def extract_log_events(log_events):
    logs_df = DataFrame(log_events, columns=[
                    'address', 'topics', 'data', 'blockNumber', 'transactionHash', 'blockHash', 'logIndex'])

    transfers_df = logs_df.loc[logs_df["topics"].str.get(
        0).isin(EVENT_SIGNATURE_HASH)]

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
        print("%s -> %s, token_id: %s, price: %s %s" % (decoder.from_address,
            decoder.to_address, str(decoder.token_id), str(decoder.price), decoder.currency))