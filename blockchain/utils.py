def format_address(address):
    if address is None:
        return None

    return  "0x" + address.lower()[-40:]