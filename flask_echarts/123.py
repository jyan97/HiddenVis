import pandas as pd

clinical_data = pd.read_csv('./test/clinical data.csv', dtype=str)
clinical_data.fillna('', inplace=True)
clinical_data.rename(columns={'Unnamed: 0':'number'}, inplace=True)

print(clinical_data.iloc[:3,:7])