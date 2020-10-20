import requests
import json
import pandas as pd
import math
import datetime
from tables.product import Product
from device_detector import DeviceDetector



class Usage:

    HTML_INDEX = 5

    def __init__(self, config):
        self.config = config


        self.rows = pd.read_csv(config.log_file)
        self.product = Product(config)
        self.products = self.product.fetch_products()


        self.url = 'https://api.airtable.com/v0/appz5xeBBomfgf2qU/Usage'



    def update(self):
        """
        Logic:
        1. Read AWS logs
        2. Iterate over logs
        3. Update the Hits count in the Product Table in Airtable
        4. Create a Usage Entry


        TODO: Error Handling
        """

        for i, row in self.rows.iterrows():
            print(f"---{i}---")

            product_id = self._product_id(row)
            if not product_id:
                continue

            resp = self.product.update_hit_count(product_id)
            resp = self._create(row, product_id)

            break










































    # Helper Functions:
    def _create(self, row, product_id):
        """
        row: each entry in the aws logs

        Logic:
        1. construct data
        2. POST call to Airtable to create an entry in USage Table
        """

        post_data = self._create_data(row, product_id)
        #print(post_data)


        resp = requests.post(self.url, data=json.dumps(post_data), headers=self.config.headers)
        print(resp.text, "\n")

        return True

    def _create_data(self, row, product_id):
        """
        Logic:
        1. Construct POST data

        TODO: Fields name should be be able to change
        """

        fields = {}

        fields['Product'] = [product_id]
        fields['Views'] = 1
        fields['Link'] = row['referrer']
        fields['Date and Time'] = self._format_time(row)
        fields['Platform'] = self._platform(row['key'])
        device = DeviceDetector(row['user_agent']).parse()
        fields['Device'] = device.os_name()

        return {"fields": fields}


    def _format_time(self, row):
        return str(datetime.datetime.strptime(row['time'], self.config.date_format))

    def _platform(self, name):
        if 'usdz' in  name:
            return 'iOS '
        return 'Web'




    def _product_id(self, row):
        """
        row -> Each row in the AWS logs.

        return product_id or empty string

        This expect name of the file to Unique

        TODO: Finding the product from name of the file.
        """

        field = self.config.product_fields[self.HTML_INDEX]
        product = 'https://swyfthome.s3-eu-west-1.amazonaws.com/' + row['key']

        # Find Product from file name
        row = self.products.loc[self.products[field] == product]
        if len(row) > 0:
            self.product_obj = row.iloc[0]
            return row.iloc[0]['id']
        else:
            return ''


