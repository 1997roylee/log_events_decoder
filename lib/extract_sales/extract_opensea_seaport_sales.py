from pandas import concat

class ExtractOpenseaSeaportSales:
    def __init__(self, df):
        """
        """
        #
        self.df = df

    def get_sales(self):
        """
        """
        # Get the sales from Opensea
        sales_df = self.get_sales_df()
        sales = self.merge_sales(sales_df, revert_sales_df)

        # Return the sales
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