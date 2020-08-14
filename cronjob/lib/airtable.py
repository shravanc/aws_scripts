import requests
import json
import pandas as pd
import math
import datetime
import json

class Airtable:
    def __init__(self, config):
        self.data = {"fields": {"Customer": "testing through script"}}
        self.headers = config.headers
        self.url = config.url
        #self.rows = pd.read_csv(config.report_file)
        self.rows = pd.read_csv(config.log_file)
        self.products = pd.read_csv(config.products_file)
        self.date = config.prefix
        self.customer = config.bucket
        self.date_format = config.date_format


    def update(self):
        for i, row in self.rows.iterrows():
            print("-----------------------------START-----------------------------------------------")
            data = self._construct_data(row)
            #print("POST---USAGE--->", data)
            self.response = requests.post(self.url, data=json.dumps(data), headers=self.headers)
            #print("USAGE_RESPONSE---->", self.response.text)
            if i > 50:
                break
            print("-----------------------------END-------------------------------------------------\n")


    def _construct_data(self, row):
        name = row['key'].split('/')[-1]
        platform = 'Web'
        if 'usdz' in  name:
            platform = 'iOS '
        else:
            Platform = 'Web'

        id = self._get_product_id(name)
        #print(f"1--name-->{name},--->id--->{id}")
        if len(id) > 1:
            resp = self.update_product_hit_count(id)

        return {"fields": { "Name": name, #row['key'].split('/')[-1],
                           "Product": [id], # ['recv7M2U0t1c1VQLO'], #name,
                           "Views": 1,
                           "Link": row['referrer'],
                           "Date and Time": self._get_time(row),
                           "Platform": platform,
                }}


    def _get_product_id(self, product):
        row = self.products.loc[self.products['value'] == product]
        print(row)
        if len(row) >0:
            return row.iloc[0]['id']
        else:
            return ''

    def _get_product_price(self, product):
        row = self.products.loc[self.products['value'] == product]
        try:
            return row.iloc[0]['Price']
        except:
            return 0.0

    def _product_price_data(self, product):
        price = product['Price']
        if price != price:
            return 0.0
        else:
            return price

    def _product_name_data(self, product):
        name = product['value']
        if name != name:
            return 'NA'
        else:
            return name

    def _get_time(self, row):
        return str(datetime.datetime.strptime(row['time'], self.date_format))


    def update_product_hit_count(self, id):
        data = self.fetch_product(id)
        #data['fields']['Hits'] += 1

        #data = {"records": [data]}
        resp = self.update_product(data)
        #print("UPDATE_RESPONSE----->", resp.text)
        return resp


    # Fetch Product by id
    def fetch_product(self, id):
        url = f"https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products/{id}"
        #print("2---->URL--->", url)
        resp = requests.get(url, headers=self.headers)
        data = json.loads(resp.text)
        #print('3--->FETCH_data--->', data)
        del data['createdTime']
        return data


    def get_patch_data(self, data):
        patch_data = {}
        patch_data['id'] = data['id']

        fields = {"Hits": data['fields']['Hits']+1}

        patch_data['fields'] = fields

        return patch_data


    def update_product(self, data):
        url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products'
        #resp = requests.patch(url, data=json.dumps(data), headers=self.headers)
        patch_data = {'records': [self.get_patch_data(data)] }
        #print("===PATCH===", patch_data)
        resp = requests.patch(url, json=patch_data
                              , headers=self.headers)
        return resp


    def create_products(self):
        ids = []
        for i, product in self.products.iterrows():
            print(product['value'])
            print(product['Price'])
            metadata = {
                "Name": self._product_name_data(product), #product['value'],
                "Price": self._product_price_data(product), #product['Price']
                "Client": ['recR3tJdG0B87xeI1'],
                "Hits": 0
            }
            data = {"fields": metadata}

            #print(data)
            self.url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products'
            self.response = requests.post(self.url, data=json.dumps(data), headers=self.headers)
            resp = json.loads(self.response.text)
            #print(resp)
            ids.append(resp['id'])


        df = pd.DataFrame({"id": ids}, columns=['id'])
        print(df.head())
        df.to_csv('/home/shravan/aws_scripts/cronjob/product_id.csv', index=False)

