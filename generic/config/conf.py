import boto3
import os
import shutil
from datetime import datetime, timedelta

from lib.clients.ez_living import EzLiving
from lib.clients.swyft import Swyft


class Config:

    def __init__(self, download=False, bucket='ez-living-logs'):

        self.download   = download
        self.bucket     = bucket
        self.prefix     = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
        self.s3_client  = boto3.client('s3')

        self.local_path = '/tmp/logs'
        if download:
            self._clean_dir(self.local_path)

        self.log_path= '/tmp/csvs'
        self._clean_dir(self.log_path)
        self.log_file = os.path.join(self.log_path, 'logs.csv')

        self.report_path = '/tmp/reports'
        self._clean_dir(self.report_path)
        self.report_file = os.path.join(self.report_path, 'report.csv')


        self.headers = {"Authorization": "Bearer key8FIuGfc4goXqdS", "Content-Type": "application/json"}

        self.client = self._get_client()


        self.names = ['bucket_owner', 'bucket', 'time', 'time_offset', 'remote_ip', 'requeste_arn', 'request_id', 'operation', 'key', 'request_uri', 'http_status', 'error_code', 'bytes_sent', 'object_size', 'total_time', 'turn_aroundtime', 'referrer', 'user_agent', 'version_id', 'host_id', 'signature_version', 'cipher_suite', 'authentication_type', 'host_header', 'tls_version']

        self.required = ['time', 'remote_ip', 'key', 'request_uri', 'http_status', 'bytes_sent', 'referrer', 'user_agent']


        # Order is important. Index of the 'AWS - HTML' is used.
        self.product_fields = ['Name', 'Price', 'Client', 'Type', 'Collection', 'AWS - HTML', 'Size (WxLxH) cm']
        self.usage_fields = ['Name', 'Product', 'Views', 'Link', 'Date and Time', 'Platform']

        self.date_format = "[%d/%b/%Y:%H:%M:%S"



    def _get_client(self):
        if self.bucket == 'ez-living-logs':
            return EzLiving()
        elif self.bucket == 'swyft-logs':
            return Swyft()
        else:
            return EzLiving()
















    def _clean_dir(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
            os.makedirs(directory)
        else:
            os.makedirs(directory)




