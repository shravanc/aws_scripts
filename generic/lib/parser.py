import os
import pandas as pd



class Parser:
    def __init__(self, config):
        self.log_file = config.log_file
        self.logs_path = config.local_path
        self.names = config.names
        #self.customer = config.bucket
        self.customer = config.client
        #self.customer = config.customer

    def clean_logs(self, df):
        df = df[~df.requeste_arn.str.contains("arn:aws:iam")]
        df = df[df.operation.str.contains("REST.GET.OBJECT")]


        df = self.customer.clean_df(df)
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
