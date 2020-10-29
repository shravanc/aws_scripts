import requests
import json
import pandas as pd
import math
import datetime
import json
import re

class Airtable:
    def __init__(self, config):
        self.config = config
        self.data = {"fields": {"Customer": "testing through script"}}
        self.headers = config.headers
        self.url = config.url
        #self.rows = pd.read_csv(config.report_file)
        self.rows = pd.read_csv(config.log_file)
        self.products = pd.read_csv(config.products_file)
        self.date = config.prefix
        self.customer = config.bucket
        self.date_format = config.date_format
        self.total_views = 0


    def swyft_report(self):
        self.all_products = self.fetch_products()
        self.all_products = self.all_products['records']
        #print(f"alll products ----> {self.all_products[0]}")

        usage = self._get_usage_details()
        self._update_revenue_report(usage)

    def _update_revenue_report(self, usage):
        print("Revenur report")
        todays_report = {
            'Client': ['recD5eJUCQBUdsqER'],
            'Number of Views Total': 0,
            'Product': [],
            'Date and Time': '2020-08-27T00:00:00',
        }

        for pr_name, data in usage.items():
            print("---data---->", data)
            todays_report['Number of Views Total'] += data['Views']
            todays_report['Product'].append(data['Products'])


        #print(todays_report)
        post_data = {
            "records": [{
                "fields": todays_report
            }]
        }
        url = 'https://api.airtable.com/v0/apptewgHCx19BU2Gh/Usage'
        print(post_data)
        resp = self._post_me(url, post_data)
        print(json.loads(resp.text))

    def _post_me(self, url, data):
        return requests.post(url, data=json.dumps(data), headers=self.headers)


    def _get_usage_details(self):
        products = []
        usage = {}
        for i, row in self.rows.iterrows():
            prod, category = self.get_product_and_category(row['referrer'])
            product = self.get_product_details(prod, category)
            pr_name = product['fields']['Name']

            update = False
            if pr_name not in usage:
                update = True
                data = {}
                data['Products'] = product['id']
            else:
                data = usage[pr_name]


            if 'Views' in data:
                data['Views'] += 1
            else:
                data['Views'] = 1




            if update:
                usage[pr_name] = data
        #print("Usage---->", usage)


        return usage

    def webflow_data(self):


        data = self.fetch_analytics()
        #print(self.all_products)

        # Total Revenue
        revenue = self.get_total_revenue()
        conversion_rate = 0.003
        todays_revenue = revenue * conversion_rate

        # Totla views
        todays_view_count = len(self.rows)

        # Analytics per Month
        if self.config.prefix.split('-')[-1] == '01':
            data['records'][0]['fields']['Revenue per Month'] = 0
            data['records'][0]['fields']['Views per Month'] = 0




        data['records'][0]['fields']['Total Views'] += todays_view_count
        data['records'][0]['fields']['Total Revenue'] += todays_revenue
        data['records'][0]['fields']['Revenue per Month'] += todays_revenue
        data['records'][0]['fields']['Views per Month'] += todays_view_count
        self._update_analytics(data)
        #print("-------------AM Done----------------", self.total_views)



    def get_total_revenue(self):

        revenue = 0
        for i, row in self.rows.iterrows():
            print(row['referrer'])
            try:
                prod, category = self.get_product_and_category(row['referrer'])
                product = self.get_product_details(prod, category)
                revenue += product['fields']['Price']
            except:
                print("******")
            break

        return revenue

    def get_product_and_category(self, url):

        arr = url.split("/")
        product = arr[-1].split("?")[0].split(".html")[0]
        category = arr[-2]

        return product, category


    def get_product_details(self, prod, category):

        for product in self.all_products:
            print("****", product)
            title = product['fields']['Name']
            pr_cat = product['fields']['category'][0]
            #print(f"{title}----{pr_cat}")
            if category == pr_cat:
                #print(f"------->{prod}---->{title}")
                if prod.lower() in title.lower():
                    #print("****Found****", product['fields']['Name'])
                    return product













    def update(self):
        for i, row in self.rows.iterrows():
            print("-----------------------------START-----------------------------------------------")
            id = self._get_product_id(name)
            if len(id) > 1:
                resp = self.update_product_hit_count(id)

            self.response = self.create_usage(row)

            print("-----------------------------END-------------------------------------------------\n")


    def _construct_data(self, row):

        name = row['key'].split('/')[-1]
        platform = self.get_platform(name)


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


    def get_platform(self, name):
        if 'usdz' in  name:
            return 'iOS '
        return 'Web'


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

    def create_usage(self, row):
         data = self._construct_data(row)
         return requests.post(self.url, data=json.dumps(data), headers=self.headers)


    def update_product_hit_count(self, id):
        data = self.fetch_product(id)
        resp = self._update_product(data)
        return resp


    def fetch_analytics(self):
        url = "https://api.airtable.com/v0/appRw2Y8QpZjYQqX1/Test?maxRecords=3&view=Grid%20view"
        resp = requests.get(url, headers=self.headers)
        return json.loads(resp.text)


    def fetch_products(self):
        #url = "https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products?maxRecords=31&view=Grid%20view"
        url = "https://api.airtable.com/v0/apptewgHCx19BU2Gh/Products?maxRecords=30&view=Grid%20view"
        resp = requests.get(url, headers=self.headers)
        return json.loads(resp.text)

    # Fetch Product by id
    def fetch_product(self, id):
        url = f"https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products/{id}"
        resp = requests.get(url, headers=self.headers)
        return json.loads(resp.text)

    #==================
    def get_analytics_data(self, data):
        patch_data = {}
        patch_data['id'] = data['id']

        fields = {"Total Views": data['fields']['Total Views'],
                  "Total Revenue": data['fields']['Total Revenue'],
                  "Revenue per Month": data['fields']['Revenue per Month'],
                  "Views per Month": data['fields']['Views per Month']}

        patch_data['fields'] = fields

        return patch_data


    def _update_analytics(self, data):
        url = "https://api.airtable.com/v0/appRw2Y8QpZjYQqX1/Test"
        #resp = requests.patch(url, data=json.dumps(data), headers=self.headers)
        patch_data = {'records': [self.get_analytics_data(data['records'][0])] }
        print("Patch Data----->", patch_data)
        #print("===PATCH===", patch_data)
        resp = requests.patch(url, json=patch_data
                              , headers=self.headers)
        return resp


    #===========================
    def get_patch_data(self, data):
        patch_data = {}
        patch_data['id'] = data['id']

        fields = {"Hits": data['fields']['Hits']+1}

        patch_data['fields'] = fields

        return patch_data


    def _update_product(self, data):
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

