from pandas import concat

class ExtractOpenseaSales:
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

        sales_df = self.get_sales_df()
        revert_sales_df = self.revert_sales_df(sales_df)
        sales = self.merge_sales(sales_df, revert_sales_df)
        return sales

    def merge_sales(self, sales, sales_db):
        """
        Merge the sales
        """
        return concat([sales, sales_db]) 
    
    def get_sales_df(self):
        """
        """
        # 
        sales_df = self.df
        sales_df['maker'] = sales_df['topics'].str.get(1)
        sales_df['taker'] = sales_df['topics'].str.get(2)
        sales_df['revert'] = False
        sales_df['price'] = sales_df['raw_log_data'].apply(
            lambda x: int(x[-64:], 16))
        return sales_df[['maker', 'taker', 'price', 'revert', 'tx_hash']]
        
    def revert_sales_df(self, sales_df):
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