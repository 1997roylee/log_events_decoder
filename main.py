from blockchain import Address

ADDRESS = "0xe6d48bf4ee912235398b96e16db6f310c21e82cb"

address_klass = Address(ADDRESS)

has_next = True

last_id = address_klass.last_transaction_page_id()

while(has_next):
    print("Page {}".format(last_id))
    transaction = address_klass.transaction.create_and_get_transactions(
        ADDRESS, last_id)

    transaction.save(last_id)
    if (transaction.has_next):
        last_id += 1
    else:
        has_next = False
