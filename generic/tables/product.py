import requests
import json
import pandas as pd
import math
import datetime



class Product:

    FILE_PATH = '/home/shravan/aws_scripts/generic/SwyftProduct.csv'

    def __init__(self, config):
        self.fetch_url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products/'
        self.update_url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products'
        self.create_url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products'

        self.config = config
        self.fields = config.product_fields


        self.create_product_csv = '/home/shravan/aws_scripts/cronjob/product_id.csv'




    def create(self, filename):
        self.products = pd.read_csv(filename)

        ids = self._create_products()
        self.products['id'] = ids

        self.products.to_csv(filename, index=False)



    def fetch_products(self):
        return pd.read_csv(self.FILE_PATH)



    def update_hit_count(self, id):
        """
        id: id of the product.


        Logic:
        ------------------------------------
        1. Fetch Product from Airtable
        2. Increment Hits Count
        3. Update the Product in new Hit count
        ------------------------------------

        TODO: Errors handling

        """
        product_data = self._retrieve_product(id)
        json_data = self._update_product_hits(product_data)

        return True









    # Helper Functions
    def _update_product_hits(self, data):
        """
        Expected data looks like below:
        {
          "id": "recloNU5y61M31108",
          "fields": {
            "Hits": 675,
          }
        }

        Hits is incremented and is updated in the Airtable.

        TODO: URL to be dynamic

        """


        updated_data = {}
        updated_data['id'] = data['id']
        updated_data['fields'] = {}
        updated_data['fields']['Hits'] = data['fields']['Hits'] + 1

        url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products'

        resp = requests.patch(url,
                              json= {'records': [updated_data]},
                              headers=self.config.headers)

        return resp


    def _retrieve_product(self, id):
        """
        id -> id of the product

        Fetch product of the specified id.

        TODO: URL to be generic enough to change
        """

        url = f"https://api.airtable.com/v0/appz5xeBBomfgf2qU/Products/{id}"
        resp = requests.get(url, headers=self.config.headers)
        return json.loads(resp.text)


    def _create_products(self):
        ids = []

        for i, product in self.products.iterrows():
            body = self._metadata(product)
            resp = requests.post(
                self.create_url,
                data=json.dumps(body),
                headers=self.config.headers
            )

            response = json.loads(resp.text)
            if response.get('id'):
                ids.append(response['id'])
            #break

        return ids


    def _metadata(self, product):
        fields = {}

        for field in self.fields:
            fields[field] = product[field]

        fields['Price'] = self._price(fields['Price'])
        fields['Client'] = [self.config.client.id]
        fields['Hits'] = 0

        return {'fields': fields}


    def _price(self, price):
        if price != price:
            return 0.0
        else:
            return float(price) #.replace(',', ''))





