from lib.config import Config
from lib.analytics import Analytics
from lib.mailer import Mailer
from lib.airtable import Airtable


# BUCKETS = ['ez-living-logs', 'meadows-and-byrne-logs', 'swyft-logs']
BUCKETS = ['ez-living-logs']
BUCKETS = ['swyft-logs']


if __name__ == "__main__":

    for bucket in BUCKETS:
        print("----Bucket----", bucket)
        config = Config(download=False, bucket=bucket)
        analytics = Analytics(config)
        analytics.generate_report()

        #print("CReport Generated---")
        #mailer = Mailer(config)
        #mailer.deliver()
        #print("Report Sent---")

        airtable = Airtable(config)
        airtable.webflow_data()
        #airtable.update()
        #airtable.create_products()
        #airtable.fetch_product('recu4alQgcx51H5JH')
        #airtable.update_product_hit_count('recu4alQgcx51H5JH')
        print("----END----")

