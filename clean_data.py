import gzip
from functools import reduce
import os
import json
from lib import TransactionDecoder, LogEventDecoder, TransferDecoder

ADDRESS = "0xb"
PATH = "./raw_transactions/%s" % (ADDRESS)


def load_files(files):
    print("Loading transactions...")
    transactions = []
    for file in files:
        print("Loading %s..." % (file))
        if file == ".DS_Store":
            continue

        with open(PATH + "/" + file) as f:
            transactions += json.loads(f.read()).get("items")
    return transactions


def clean_transactions(transactions):
    print("Cleaning transactions...")
    cleaned_transactions = []
    for transaction in transactions:
        cleaned_transactions.append(TransactionDecoder(transaction))
    return cleaned_transactions


files = os.listdir(PATH)
transactions = load_files(files)

cleaned_transactions = clean_transactions(transactions)
cleaned_log_events = list(map(
    lambda cleaned_transaction: cleaned_transaction.log_events, cleaned_transactions))
cleaned_log_events = sum(cleaned_log_events, [])

df = LogEventDecoder.to_data_frame(cleaned_log_events)

arr = []
with gzip.open("output/{}".format(ADDRESS + ".json.gz"), 'w') as f:
    for index, row in df.nft_transfers().iterrows():
        decoder = TransferDecoder(row)
        # print("%s -> %s, token_id: %s, price: %s %s, tx_hash: %s" % (decoder.from_address,
        #                                                             decoder.to_address, str(decoder.token_id), str(decoder.price), decoder.currency, decoder.transaction_hash))
        arr.append(decoder.to_json())
    f.write(json.dumps(arr).encode('utf-8'))
