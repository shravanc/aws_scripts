from lib.config import Config
from lib.analytics import Analytics
from lib.mailer import Mailer
from lib.airtable import Airtable


BUCKETS = ['ez-living-logs', 'meadows-and-byrne-logs', 'swyft-logs']


if __name__ == "__main__":

    for bucket in BUCKETS:
        config = Config(download=True, bucket)
        analytics = Analytics(config)
        analytics.generate_report()

        #print("CReport Generated---")
        #mailer = Mailer(config)
        #mailer.deliver()
        #print("Report Sent---")

        airtable = Airtable(config)
        airtable.update()

