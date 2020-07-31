import requests
import json
import pandas as pd

class Airtable:
    def __init__(self, config):
        self.data = {"fields": {"Customer": "testing through script"}}
        self.headers = config.headers
        self.url = config.url
        self.rows = pd.read_csv(config.report_file)
        self.date = config.prefix


    def update(self):
        for i, row in self.rows.iterrows():
            self.response = requests.post(self.url, data=json.dumps(self._construct_data(row)), headers=self.headers)


    def _construct_data(self, row):
        return { "fields": { "Customer": 'Ez-Living',
                "Product": row['key'].split('/')[-1],
                "Views": row['hits'],
                "Link": row['referee'],
                "Date and Time": self.date
                }}
