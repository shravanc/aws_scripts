from lib.config import Config
from lib.analytics import Analytics
from lib.mailer import Mailer
from lib.airtable import Airtable

if __name__ == "__main__":
    config = Config(download=False) #True)
    analytics = Analytics(config)
    analytics.generate_report()

    #print("CReport Generated---")
    #mailer = Mailer(config)
    #mailer.deliver()
    #print("Report Sent---")

    airtable = Airtable(config)
    airtable.update()

