from pandas import concat


APE_COLLECTION = ["0xe6d48bf4ee912235398b96e16db6f310c21e82cb"]


class OpenseaSeaportSaleExtractor(object):
    def __init__(self, df):
        """
        """
        #
        self.df = df

    def get_sales(self):
        """
        """
        # Get the sales from Opensea
        if self.df.empty:
            return self.df

        sales_df = self._get_sales_df()
        revert_sales_df = self._revert_sales_df(sales_df)
        sales_df = self._merge_sales(sales_df, revert_sales_df)
        return sales_df

    def _merge_sales(self, af, bf):
        return concat([af, bf])

    def _split_raw_data(self, raw_data, n=64):
        return [(raw_data[i:i+n]) for i in range(0, len(raw_data), n)]

    def _extract_from_address(self, raw_log_data):
        return "0x" + self._split_raw_data(raw_log_data[2:])[1]

    def _extract_raw_transfer_group(self, raw_log_data):
        raw_list = self._split_raw_data(raw_log_data[2:])
        group_a = raw_list[6:9]
        group_b = raw_list[11:14]
        group_c = raw_list[16:19]
        group_d = raw_list[21:24]
        return [group_a, group_b, group_c, group_d]

    def _extract_collection_group(self, raw_transfer_group):
        indexes = [i for i, _ in enumerate(raw_transfer_group) if len(_) > 0 and hex(
            int(_[0], 16)) in APE_COLLECTION]
        if len(indexes) == 0:
            return None, None
        else:
            return raw_transfer_group[indexes[0]], indexes[0]

    def _extract_price(self, raw_log_data):
        groups = self._extract_raw_transfer_group(raw_log_data)
        collection_group, index = self._extract_collection_group(groups)
        if index is not None:
            del groups[index]
        return sum(map(lambda x: int(x[2], 16) if len(x) > 0 else 0, groups))

    def _get_sales_df(self):
        """
        """
        #
        sales_df = self.df.copy()
        sales_df['taker'] = sales_df['raw_log_data'].apply(
            lambda x: self._extract_from_address(x))
        sales_df['revert'] = False
        sales_df['price'] = sales_df['raw_log_data'].apply(
            lambda x: self._extract_price(x))
        sales_df['maker'] = sales_df['topics'].str.get(1)
        return sales_df[['maker', 'taker', 'price', 'revert', 'transaction_hash']]

    def _revert_sales_df(self, sales_df):
        """
        """
        #
        revert_sales_df = sales_df.copy()
        revert_sales_df['revert'] = True
        taker = revert_sales_df['taker']
        maker = revert_sales_df['maker']
        revert_sales_df['maker'] = taker
        revert_sales_df['taker'] = maker
        return revert_sales_df
