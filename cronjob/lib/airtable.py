import requests
import json
import pandas as pd
import math
class Airtable:
    def __init__(self, config):
        self.data = {"fields": {"Customer": "testing through script"}}
        self.headers = config.headers
        self.url = config.url
        self.rows = pd.read_csv(config.report_file)
        self.products = pd.read_csv(config.products_file)
        self.date = config.prefix
        self.customer = config.bucket


    def update(self):
        for i, row in self.rows.iterrows():
            data = self._construct_data(row)
            price = self._get_product_price(data['fields']['Product'])
            if math.isnan(price):
                data['fields']['Price'] = 0.0
            else:
                data['fields']['Price'] = price
            self.response = requests.post(self.url, data=json.dumps(data), headers=self.headers)
            #print("----code---->", self.response.status_code)
            print("----code---->", self.response.text)


    def _construct_data(self, row):
        return {"fields": { "Client": self.customer,
                "Product": row['key'].split('/')[-1],
                "Views": row['hits'],
                "Link": row['referee'],
                "Date and Time": self.date
                }}

    def _get_product_price(self, product):
        row = self.products.loc[self.products['value'] == product]
        try:
            return row.iloc[0]['Price']
        except:
            return 0.0
