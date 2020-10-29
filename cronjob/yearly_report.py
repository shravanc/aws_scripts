from lib.config import Config
from lib.analytics import Analytics
from lib.mailer import Mailer
from lib.airtable import Airtable
from datetime import timedelta, date


# BUCKETS = ['ez-living-logs', 'meadows-and-byrne-logs', 'swyft-logs']
BUCKETS = ['ez-living-logs']
BUCKETS = ['swyft-logs']

START_DATE  = date(2020, 1, 1)
END_DATE    = date(2020, 10, 28)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)







if __name__ == "__main__":

    for bucket in BUCKETS:
        config = Config(download=True, bucket=bucket)

        for single_date in daterange(START_DATE, END_DATE):
            day = single_date.strftime("%Y-%m-%d")
            try:
                config.prefix = day
                analytics = Analytics(config)
                analytics.download_logs()
            except:
                print(f"----ERROR---->{day}")

        #analytics.generate_report()

        #airtable.update()
        #airtable.create_products()
        #airtable.fetch_product('recu4alQgcx51H5JH')
        #airtable.update_product_hit_count('recu4alQgcx51H5JH')
        print("----END----")

