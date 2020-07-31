import boto3
import os
import shutil
from datetime import datetime


class Config:
    def __init__(self, download=False, bucket='ez-living-logs'):
        self.download = download
        self.bucket = bucket
        self.prefix = datetime.today().strftime('%Y-%m-%d')
        self.client = boto3.client('s3')

        self.local_path = '/tmp/logs'
        if download:
            self.clean_dir(self.local_path)

        self.log_path= '/tmp/csvs'
        self.clean_dir(self.log_path)
        self.log_file = os.path.join(self.log_path, 'logs.csv')

        self.report_path = '/tmp/reports'
        self.clean_dir(self.report_path)
        self.report_file = os.path.join(self.report_path, 'report.csv')


        self.names = ['bucket_owner', 'bucket', 'time', 'time_offset', 'remote_ip', 'requeste_arn', 'request_id', 'operation', 'key', 'request_uri', 'http_status', 'error_code', 'bytes_sent', 'object_size', 'total_time', 'turn_aroundtime', 'referrer', 'user_agent', 'version_id', 'host_id', 'signature_version', 'cipher_suite', 'authentication_type', 'host_header', 'tls_version']

        self.required = ['time', 'remote_ip', 'key', 'request_uri', 'http_status', 'bytes_sent', 'referrer', 'user_agent']

        self.fromaddr = 'no.place.like.co@gmail.com'
        self.toaddr = 'shravan007.c@gmail.com'
        self.emails = ['shravan007.c@gmail.com', 'allen@noplacelike.co']
        self.password = 'N0Pl@ceL!ke'

        self.headers = {"Authorization": "Bearer key8FIuGfc4goXqdS", "Content-Type": "application/json"}
        self.url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/EZ%20Living%20Interiors'

        self.products = os.path.join(os.getcwd(), 'products.csv')


    def clean_dir(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
            os.makedirs(directory)
        else:
            os.makedirs(directory)

