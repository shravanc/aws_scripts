import pandas as pd


sfile = '/home/shravan/aws_scripts/cronjob/products.csv'
id_file = '/home/shravan/aws_scripts/cronjob/product_id.csv'

source = pd.read_csv(sfile)
id = pd.read_csv(id_file)
source['id'] = id['id']

source.to_csv('/home/shravan/aws_scripts/cronjob/final.csv', index=False)
