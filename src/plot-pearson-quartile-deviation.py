import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input pearson matrix file")
parser.add_argument("raf", help="raf-pos file")
parser.add_argument("out", help="output file")

args = parser.parse_args()

raf_base = pd.read_csv('/raf_pos.csv',sep=',')
iqs = pd.read_csv(args.input)
raf_pos = pd.read_csv(args.raf,sep=";")
raf = pd.merge(raf_base,raf_pos,how='inner', on=['POS','REF','ALT'])
raf = raf[['POS','RAF_x']]
raf = raf.reset_index(drop=True)
data = pd.concat([iqs,raf],axis=1)
data = data.sort_values(by='RAF_x')
data = data.reset_index(drop=True)
def quartile_deviation(data):
    q1 = np.quantile(data,0.05)
    q2 = np.quantile(data,0.5)
    q3 = np.quantile(data,0.95)
    return (q2-q1),(q3-q2)

i= data.index
ind = data['RAF_x']<= 0.001
index_1 = i[ind]
ind = data['RAF_x']<= 0.005
index_2 = i[ind]
ind = data['RAF_x']<= 0.01
index_3 = i[ind]
ind = data['RAF_x']<= 0.05
index_4 = i[ind]
ind = data['RAF_x']<= 0.1
index_5 = i[ind]
ind = data['RAF_x']<= 0.5
index_6 = i[ind]

dev_001_1,dev_001_2 = quartile_deviation(np.sort(np.array(data.loc[0:index_1.max()+1,"PCOR"].values.tolist())))
dev_005_1,dev_005_2 = quartile_deviation(np.sort(np.array(data.loc[index_1.max():index_2.max()+1,'PCOR'].values.tolist())))
dev_01_1,dev_01_2 = quartile_deviation(np.sort(np.array(data.loc[index_2.max():index_3.max()+1,'PCOR'].values.tolist())))
dev_05_1,dev_05_2 = quartile_deviation(np.sort(np.array(data.loc[index_3.max():index_4.max()+1,'PCOR'].values.tolist())))
dev_1_1,dev_1_2 = quartile_deviation(np.sort(np.array(data.loc[index_4.max():index_5.max()+1,'PCOR'].values.tolist())))
dev_5_1,dev_5_2 = quartile_deviation(np.sort(np.array(data.loc[index_4.max():index_6.max()+1,'PCOR'].values.tolist())))
dev1_1,dev1_2 = quartile_deviation(np.sort(np.array(data.loc[index_6.max():,'PCOR'].values.tolist())))
print('Deviation:   ', dev_001_1,dev_001_2,dev_005_1,dev_005_2,dev_01_1,dev_01_2,dev_05_1,dev_05_2,dev_1_1,dev_1_2,dev_5_1,dev_5_2,dev1_1,dev1_2)
print("PCOR:     0.001: ",data.loc[0:index_1.max()+1,"PCOR"].median(),"0.005: ",data.loc[index_1.max():index_2.max()+1,'PCOR'].median(),
        "0.01: ", data.loc[index_2.max():index_3.max()+1,'PCOR'].median(),"0.05    ",data.loc[index_3.max():index_4.max()+1,'PCOR'].median(),
        "0.1:   ", data.loc[index_4.max():index_5.max()+1,'PCOR'].median(),"0.5   ",data.loc[index_4.max():index_6.max()+1,'PCOR'].median(),
        "1.0:   ",data.loc[index_6.max():,'PCOR'].median())

maf = [0.001,0.005,0.01,0.05,0.1,0.5,1.0]
values = [data.loc[0:index_1.max()+1,"PCOR"].median(),data.loc[index_1.max():index_2.max()+1,'PCOR'].median(), data.loc[index_2.max():index_3.max()+1,'PCOR'].median(),
          data.loc[index_3.max():index_4.max()+1,'PCOR'].median(), data.loc[index_4.max():index_5.max()+1,'PCOR'].median(),data.loc[index_4.max():index_6.max()+1,'PCOR'].median(),data.loc[index_6.max():,'PCOR'].median()]
dev1 = [dev_001_1,dev_005_1,dev_01_1,dev_05_1,dev_1_1,dev_5_1,dev1_1]
dev2 = [dev_001_2,dev_005_2,dev_01_2,dev_05_2,dev_1_2,dev_5_2,dev1_2]

count = [data.loc[0:index_1.max()+1,"PCOR"].count(),data.loc[index_1.max():index_2.max()+1,'PCOR'].count(),
         data.loc[index_2.max():index_3.max()+1,'PCOR'].count(),data.loc[index_3.max():index_4.max()+1,'PCOR'].count(),
         data.loc[index_4.max():index_5.max()+1,'PCOR'].count(),data.loc[index_4.max():index_6.max()+1,'PCOR'].count(),
         data.loc[index_6.max():,'PCOR'].count()]



tmp = {'maf':maf,'values':values,'deviation1':dev1,'deviation2':dev2, 'count':count}
file = pd.DataFrame(tmp)

file.to_csv(args.out,index = False)
print("Done")
#plt.plot([0.001,0.005,0.01,0.05,0.1,0.5,1.0],[data.loc[0:index_1.max()+1,"PCOR"].median(),data.loc[index_1.max():index_2.max()+1,'PCOR'].median(),
#data.loc[index_2.max():index_3.max()+1,'PCOR'].median(),data.loc[index_3.max():index_4.max()+1,'PCOR'].median(),
#data.loc[index_4.max():index_5.max()+1,'PCOR'].median(),data.loc[index_4.max():index_6.max()+1,'PCOR'].median(),
#data.loc[index_6.max():,'PCOR'].median()],marker='o')
#plt.xlabel("MAF")
#plt.ylabel("Pearson Correlation")
#plt.savefig("/data/pcor.png")
