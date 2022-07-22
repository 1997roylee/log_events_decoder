from pandas import concat
from blockchain.utils import format_address

class OpenseaSaleExtractor(object):
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
        sales = self._merge_sales(sales_df, revert_sales_df)
        return sales

    def _merge_sales(self, sales_df, revert_sales_df):
        """
        Merge the sales
        """
        return concat([sales_df, revert_sales_df])

    def _get_sales_df(self):
        """
        """
        #
        sales_df = self.df.copy()
        sales_df['maker'] = sales_df['topics'].str.get(1).apply(lambda x: format_address(x))
        sales_df['taker'] = sales_df['topics'].str.get(2).apply(lambda x: format_address(x))
        sales_df['revert'] = False
        sales_df['price'] = sales_df['raw_log_data'].apply(
            lambda x: int(x[-64:], 16))
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
