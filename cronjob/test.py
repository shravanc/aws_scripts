import pandas as pd

df = pd.read_csv("./products.csv")
print(df.head())
for i, row in df.iterrows():
    if str(row['value']) != 'nan':
        text = row['value'].split('/')[-1].replace(".usdz'", '.usdz').replace(".glb'", '.glb')
        #df.iloc[i]['value'] = text
        df.at[i, 'value'] = text




df.to_csv('./test.csv', index=False)
