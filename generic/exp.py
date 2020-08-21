import pandas as pd

df = pd.read_csv("./products.csv")
a = df[df['value'] == 'EZLivingInteriors_-_Kendal3SeaterBlue.usdz']
print(a)
