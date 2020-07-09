import os
import pandas as pd

class Parser:
  def __init__(self, config):
    self.log_file = config.log_file
    self.logs_path = config.local_path
    self.names = config.names


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
    print(len(df))
 
    df.to_csv(self.log_file, index=False)
