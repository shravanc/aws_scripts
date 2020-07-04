import pandas as pd

def valid(row):
    if row['HTTP status'] != 200:
        return False

    if row['Key'] == '-':
        return False

    if row['Request-URI'].split(' ')[0] != 'GET':
        return False

    return True


def process(df):
    data = []
    hifen_count = 0
    for index, row in df.iterrows():
        if not valid(row):
            continue

        key, referee = row[ ['Key', 'Referrer'] ]
        if referee == '-':
            hifen_count += 1
        data.append([key, referee, 1])

    print(hifen_count)
    return data


def analyse(fname, path):
    df = pd.read_csv(fname)
    data = process(df)
    new_df = pd.DataFrame(data, columns=['key', 'referee', 'hits'])

    final = new_df.groupby(
        ['key', 'referee']
    ).sum()

    final.to_csv(path)


"""
url = './csvs/June_1_2020.csv'
path = './csvs/report.csv'
analyse(url)
"""
