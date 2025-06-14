import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input pearson matrix file")
parser.add_argument("raf", help="raf-pos file")
parser.add_argument("out", help="output file")

args = parser.parse_args()

iqs = pd.read_csv(args.input)
raf = pd.read_csv(args.raf,sep=";")
data = pd.concat([iqs,raf],axis=1)
data = data.sort_values(by='RAF')
data = data.reset_index(drop=True)

i= data.index
ind = data['RAF']<= 0.001
index_1 = i[ind]
ind = data['RAF']<= 0.005
index_2 = i[ind]
ind = data['RAF']<= 0.01
index_3 = i[ind]
ind = data['RAF']<= 0.05
index_4 = i[ind]
ind = data['RAF']<= 0.1
index_5 = i[ind]
ind = data['RAF']<= 0.5
index_6 = i[ind]

print("0.001: ",data.loc[0:index_1.max()+1,"PCOR"].mean(),"0.05: ",data.loc[index_1.max():index_2.max()+1,'PCOR'].mean(),
        "0.01: ", data.loc[index_2.max():index_3.max()+1,'PCOR'].mean(),"0.05    ",data.loc[index_3.max():index_4.max()+1,'PCOR'].mean(),
        "0.1:   ", data.loc[index_4.max():index_5.max()+1,'PCOR'].mean(),"0.5   ",data.loc[index_4.max():index_6.max()+1,'PCOR'].mean(),
        "1.0:   ",data.loc[index_6.max():,'PCOR'].mean())
print("0.001: ",data.loc[0:index_1.max()+1,"PCOR"].std(),"0.05: ",data.loc[index_1.max():index_2.max()+1,'PCOR'].std(),
        "0.01: ", data.loc[index_2.max():index_3.max()+1,'PCOR'].std(),"0.05    ",data.loc[index_3.max():index_4.max()+1,'PCOR'].std(),
        "0.1:   ", data.loc[index_4.max():index_5.max()+1,'PCOR'].std(),"0.5   ",data.loc[index_4.max():index_6.max()+1,'PCOR'].std(),
        "1.0:   ",data.loc[index_6.max():,'PCOR'].std())
print("0.001: ",data.loc[0:index_1.max()+1,"PCOR"].count(),"0.05: ",data.loc[index_1.max():index_2.max()+1,'PCOR'].count(),
        "0.01: ", data.loc[index_2.max():index_3.max()+1,'PCOR'].count(),"0.05    ",data.loc[index_3.max():index_4.max()+1,'PCOR'].count(),
        "0.1:   ", data.loc[index_4.max():index_5.max()+1,'PCOR'].count(),"0.5   ",data.loc[index_4.max():index_6.max()+1,'PCOR'].count(),
        "1.0:   ",data.loc[index_6.max():,'PCOR'].count())


maf = [0.001,0.005,0.01,0.05,0.1,0.5,1.0]
values = [data.loc[0:index_1.max()+1,"PCOR"].mean(),data.loc[index_1.max():index_2.max()+1,'PCOR'].mean(), data.loc[index_2.max():index_3.max()+1,'PCOR'].mean(),
          data.loc[index_3.max():index_4.max()+1,'PCOR'].mean(), data.loc[index_4.max():index_5.max()+1,'PCOR'].mean(),data.loc[index_4.max():index_6.max()+1,'PCOR'].mean(),
          data.loc[index_6.max():,'PCOR'].mean()]
std =[data.loc[0:index_1.max()+1,"PCOR"].std(),data.loc[index_1.max():index_2.max()+1,'PCOR'].std(),
      data.loc[index_2.max():index_3.max()+1,'PCOR'].std(),data.loc[index_3.max():index_4.max()+1,'PCOR'].std(),
      data.loc[index_4.max():index_5.max()+1,'PCOR'].std(),data.loc[index_4.max():index_6.max()+1,'PCOR'].std(),
      data.loc[index_6.max():,'PCOR'].std()]
count = [data.loc[0:index_1.max()+1,"PCOR"].count(),data.loc[index_1.max():index_2.max()+1,'PCOR'].count(),
         data.loc[index_2.max():index_3.max()+1,'PCOR'].count(),data.loc[index_3.max():index_4.max()+1,'PCOR'].count(),
         data.loc[index_4.max():index_5.max()+1,'PCOR'].count(),data.loc[index_4.max():index_6.max()+1,'PCOR'].count(),
         data.loc[index_6.max():,'PCOR'].count()]



tmp = {'maf':maf,'values':values,'std':std, 'count':count}
file = pd.DataFrame(tmp)

file.to_csv(args.out,index = False)

plt.plot([0.001,0.005,0.01,0.05,0.1,0.5,1.0],[data.loc[0:index_1.max()+1,"PCOR"].mean(),data.loc[index_1.max():index_2.max()+1,'PCOR'].mean(),
data.loc[index_2.max():index_3.max()+1,'PCOR'].mean(),data.loc[index_3.max():index_4.max()+1,'PCOR'].mean(),
data.loc[index_4.max():index_5.max()+1,'PCOR'].mean(),data.loc[index_4.max():index_6.max()+1,'PCOR'].mean(),
data.loc[index_6.max():,'PCOR'].mean()],marker='o')
plt.xlabel("MAF")
plt.ylabel("Pearson Correlation")
plt.savefig("pcor.png")
