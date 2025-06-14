import pandas as  pd

data = pd.read_csv('data/imputed-600-sas.csv',sep=';',usecols=['POS','RAF','REF','ALT'])
data.to_csv('data/raf_pos.csv',index=False)

