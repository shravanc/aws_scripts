class Swyft:

    def __init__(self):
        self.id = 'recJWfHOBHW0SNqou'
        self.df = None

    def clean_df(self, df):
        self.df = df[df.request_uri.str.contains(".html", case=False)]
        return self.df
