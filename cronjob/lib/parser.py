import os
import pandas as pd



class Parser:
    def __init__(self, config):
        self.log_file = config.log_file
        self.logs_path = config.local_path
        self.names = config.names
        self.customer = config.bucket

    def clean_logs(self, df):
        df = df[~df.requeste_arn.str.contains("arn:aws:iam")]

        # Filter only REST.GET.OBJECT
        df = df[df.operation.str.contains("REST.GET.OBJECT")]

        # Filter Bots and Scralers
        #df = df[~df.request_uri.str.contains("favicon")]
        #df = df[~df.request_uri.str.contains("robots")]
        #df = df[~df.request_uri.str.contains("wp-login.php")]
        #df = df[~df.user_agent.str.contains("bot", case=False)]
        #df = df[~df.user_agent.str.contains("crawler", case=False)]

        # Filter to get only glb, usdz
        # df = df[~df.request_uri.str.contains(".css", case=False)]
        # df = df[~df.request_uri.str.contains(".js", case=False)]
        if self.customer == 'swyft-logs':
            df = df[~df.request_uri.str.contains(".html", case=False)]
        #df = df[df.request_uri.str.contains(".usdz", case=False)]
        return df

    def parse(self):
        df_list = []
        for index, file in enumerate(os.listdir(self.logs_path)):
            log = os.path.join(self.logs_path, file)
            df = pd.read_csv(log, delimiter=' ')
            df_list.append(pd.read_csv(
                log,
                sep=" ",
                names=self.names,
            ))

        df = pd.concat(df_list)  # concatenate all df
        df = self.clean_logs(df)
        df.to_csv(self.log_file, index=False)
