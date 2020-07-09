import boto3
import os
import shutil

from download_s3_log_files import download_dir
from parse import parse_logs
from create_report import analyse
from config import Config


def clean_dir(directory):

  if os.path.exists(directory):
    shutil.rmtree(directory)
    os.makedirs(directory)
  else:
    os.makedirs(directory)


if __name__ == '__main__':
  config = Config()
  prefix = '2020-06-14'
  bucket = 'ez-living-logs'
  local = '/tmp/logs'
  clean_dir(local)
  s3_client = boto3.client('s3')

  # Download
  download_dir(config, s3_client)
  #download_dir(prefix, local, bucket, s3_client)

  csv_path = '/tmp/csvs'
  clean_dir(csv_path)
  parsed_file = os.path.join(csv_path, 'logs.csv')

  # Parse
  parse_logs(local, parsed_file)

  report_path = '/tmp/reports'
  clean_dir(report_path)

  
  # Analyse
  report = os.path.join(report_path, 'report.csv')
  analyse(parsed_file, report)


