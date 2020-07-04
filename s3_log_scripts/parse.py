import pandas as pd
import os


#path = './logs'

def parse_logs(path, csv_file):
  df_list = []
  for index, file in enumerate(os.listdir(path)):
    log = os.path.join(path, file)
    df = pd.read_csv(log, delimiter=' ')
    df_list.append(pd.read_csv(
        log,
        sep=" ",
        names=['Bucket Owner', 'Bucket', 'Time', 'Time - Offset', 'Remote IP', 'Requester ARN/Canonical ID', 'Request ID', 'Operation', 'Key', 'Request-URI', 'HTTP status', 'Error Code', 'Bytes Sent', 'Object Size', 'Total Time', 'Turn-Around Time', 'Referrer', 'User-Agent', 'Version Id', 'Host Id', 'Signature Version', 'Cipher Suite', 'Authentication Type', 'Host Header', 'TLS version'],
    ))


  df = pd.concat(df_list)  # concatenate all df
  print(len(df))

  df.to_csv(csv_file, index=False)

