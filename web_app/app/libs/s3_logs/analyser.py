import pandas as pd
class Analyser:

  def __init__(self, config):
    self.log_file = config.log_file
    self.report_file = config.report_file


  def valid(self, row):
    if row['http_status'] != 200:
        return False

    if row['key'] == '-':
        return False

    if row['request_uri'].split(' ')[0] != 'GET':
        return False

    return True


  def process(self, df):
    data = []
    hifen_count = 0
    for index, row in df.iterrows():
        if not self.valid(row):
            continue

        key, referee = row[ ['key', 'referrer'] ]
        if referee == '-':
            hifen_count += 1
        data.append([key, referee, 1])

    print(hifen_count)
    return data

  def analyse(self):
    df = pd.read_csv(self.log_file)
    data = self.process(df)
    new_df = pd.DataFrame(data, columns=['key', 'referee', 'hits'])

    final = new_df.groupby(
        ['key', 'referee']
    ).sum()

    final.to_csv(self.report_file)

