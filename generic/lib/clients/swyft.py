class Swyft:

    def __init__(self):
        self.df = None

    def clean_df(self, df):
        self.df = df[~df.request_uri.str.contains(".html", case=False)]
        return df
