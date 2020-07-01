import pandas as pd
import csv

url = './June_1_2020.csv'
df = pd.read_csv(url)

path = './referer_2.csv'
error_path = './errors.csv'
er_file = open(error_path, mode='w')
er_writer = csv.writer(er_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
er_writer.writerow(
    ['Bucket Owner', 'Bucket', 'Time', 'Time - Offset', 'Remote IP', 'Requester ARN/Canonical ID', 'Request ID',
     'Operation', 'Key', 'Request-URI', 'HTTP status', 'Error Code', 'Bytes Sent', 'Object Size', 'Total Time',
     'Turn-Around Time', 'Referrer', 'User-Agent', 'Version Id', 'Host Id', 'Signature Version', 'Cipher Suite',
     'Authentication Type', 'Host Header', 'TLS version'])


def verify_data(row):
    if row['HTTP status'] != 200:
        return False

    if row['Key'] == '-':
        return False

    if row['Request-URI'].split(' ')[0] != 'GET':
        return False

    return True


with open(path, mode='w') as fp:
    csv_writer = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['referer', 'hits', 'bytes'])

    referees = {}
    for index, row in df.iterrows():

        if not verify_data(row):
            er_writer.writerow(row.to_list())
            continue

        if referees.get(row['Referrer']):
            referees[row['Referrer']] += 1
        else:
            referees[row['Referrer']] = 1

    for k, v in referees.items():
        csv_writer.writerow([k, v])

er_file.close()
