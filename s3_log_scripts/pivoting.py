import pandas as pd
import csv
import numpy as np


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
    for index, row in df.iterrows():
        if not valid(row):
            continue

        key, referee = row[fields]

        data.append([key, referee, 1])
    return data


# def get_csv_data(keys):
#     csv_data = []
#     for k, v in keys.items():
#         csv_data.append([k, v[]])

def analyse(fname):
    df = pd.read_csv(fname)
    data = process(df)
    new_df = pd.DataFrame(data, columns=['key', 'referee', 'hits'])
    # ptable = new_df.pivot_table(
    #     values='key',
    #     index='referee',
    #     columns='hits',
    #     aggfunc=np.sum
    # )

    final = new_df.groupby(
        ['key', 'referee',]
    ).sum()

    print(final)
    final.to_csv(path)



fields = ['Key', 'Referrer']

url = './June_1_2020.csv'
path = './pivot.csv'
analyse(url)