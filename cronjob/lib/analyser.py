import pandas as pd
class Analyser:

    def __init__(self, config):
        self.log_file = config.log_file
        self.report_file = config.report_file
        self.valid_count = 0
        self.invalid_count = 0
        self.hifen_count = 0

    def valid(self, row):
        if 'arn:aws:iam' in row['requeste_arn']:
          return False

        if row['http_status'] != 200:
            return False

        if row['key'] == '-':
            return False

        if row['request_uri'].split(' ')[0] != 'GET':
            return False

        return True


    def process(self, df):
        data = []
        self.hifen_count = 0
        for index, row in df.iterrows():
            if not self.valid(row):
                self.invalid_count += 1
                continue

            key, referee = row[ ['key', 'referrer'] ]
            if referee == '-':
                self.hifen_count += 1
            data.append([key, referee, 1])
            self.valid_count += 1

        return data

    def analyse(self):
        df = pd.read_csv(self.log_file)
        data = self.process(df)
        new_df = pd.DataFrame(data, columns=['key', 'referee', 'hits'])

        final = new_df.groupby(
            ['key', 'referee']
        ).sum()

        final.to_csv(self.report_file)

        with open('./report.txt', mode='w+') as fp:
          fp.write(f"Valid_Count: {self.valid_count}\n")
          fp.write(f"Invalid_Count: {self.invalid_count}\n")
          fp.write(f"Hiphen Count: {self.hifen_count}\n")

