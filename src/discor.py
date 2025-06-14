import pandas as pd
import numpy as np
import dcor
from multiprocessing import Pool

class DisCor:
    def __init__(self):
        pass

    def prob_calc(self, imp_data,true_data ):
        count =0.0
        tmp =0.0
        for i in range(len(imp_data)):
            if true_data[i] =='./.' or true_data[i]=='.|.':
                continue
            else:
                imp_val = [float(x) for x in imp_data[i].split(',')]
                true_val = [float (x) for x in true_data[i].split(',')]
                tmp = tmp + dcor.distance_correlation(np.array(imp_val),np.array(true_val))
                count = count+1.0
            dis_cor = tmp/count
        return dis_cor


    def discor_table(self,imp_true_data):
        '''This function will genereate IQS martix for the whole vcf'''
        discor_matrix = pd.DataFrame(columns=['DCOR'])
        count =0
        for row in imp_true_data.itertuples(index=False):
            discor = self.prob_calc(row[:100],row[100:])
            discor_matrix.loc[len(discor_matrix)]=[discor]
        return discor_matrix['DCOR']


if __name__ == "__main__":
    genotype_confusion_matrix = pd.read_csv('data/genotype_confusion_matrix.csv',sep=';',chunksize=14000)
    discor_matrix = pd.DataFrame(columns=['DCOR'])
    with Pool(processes=16) as pool:
        discor = DisCor()
        discor_list = pool.map(discor.discor_table, genotype_confusion_matrix)
        discor_matrix = pd.concat(discor_list, ignore_index=True)
    discor_matrix.to_csv('data/discor_test.csv', sep=',', encoding='utf-8',index=False)
