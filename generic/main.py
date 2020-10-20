from config.conf import Config
from lib.analytics import Analytics
from lib.mailer import Mailer
from lib.airtable import Airtable



from tables.product import Product
from tables.usage import Usage

# BUCKETS = ['ez-living-logs', 'meadows-and-byrne-logs', 'swyft-logs']
# BUCKETS = ['ez-living-logs']
BUCKETS = ['swyft-logs']

if __name__ == "__main__":

    for bucket in BUCKETS:
        config = Config(download=True, bucket=bucket)
        analytics = Analytics(config)
        analytics.generate_report()

        # product = Product(config)
        # filename = '/home/shravan/aws_scripts/generic/SwyftProduct.csv'
        # product.create(filename)

        print("---starting---")
        usage = Usage(config)
        usage.update()



