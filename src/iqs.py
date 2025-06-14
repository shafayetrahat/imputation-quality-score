import pandas as pd
#import numpy as np
from multiprocessing import Pool

class IQS:
    def __init__(self):
        '''This class calculates the imputation quality score between true and imputed genoytpe from imputed genotype
        probability. For details, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0137601 and https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009697'''
        pass
    def iqs_calc(self,p0,pc):
        '''This function will calculate IQS. IQS = (p_o-p_c)/(1-p_c)'''
        if p0==pc:
            return p0
        else:
            iqs = (p0-pc)/(1.0-pc)
            return iqs
    def multiply_matrix(self,imp,true):
        result = [[0 for col in range(3)] for row in range(3)]
        for row in range(len(imp)):
            for col in range(len(true)):
                result[row][col]=imp[row]*true[col]
        n = [result[0][i]+result[1][i]+result[2][i] for i in range(3)]
        pc = [result[i][0]+result[i][1]+result[i][2] for i in range(3)]
        po = result[0][0]+result[1][1]+result[2][2]
        return n,pc,po

    def prob_calc(self, imp_data,true_data ):
        '''observing probabilty for IQS. p_o=sum(p_o11+p_o22+p_o33)'''
        pc = pc1 = pc2 = pc3 = p0 = N0 = N1 = N2 = N3 = N = 0.0
        for i in range(len(imp_data)):
            if true_data[i] =='./.' or true_data[i] =='.|.':
                N0 = N0+1.0
                continue
            else:
                imp_val = [float(x) for x in imp_data[i].split(',')]
                true_val = [float (x) for x in true_data[i].split(',')]
                n,pc0,po = self.multiply_matrix(imp_val,true_val)
                N1 = N1+n[0]
                N2 = N2+n[1]
                N3 = N3+n[2]
                pc1 = pc0[0]+pc1
                pc2 = pc0[1]+pc2
                pc3 = pc0[2]+pc3
                p0 = p0+po
        N = len(imp_data)-N0
        pc = (N1*pc1+N2*pc2+N3*pc3)/(N*N)
        p0 = p0/N
        return self.iqs_calc(p0,pc)
#
#


    def iqs_table(self,imp_true_data):
        '''This function will genereate IQS martix for the whole vcf'''
        iqs_matrix = pd.DataFrame(columns=['IQS'])
        count =0
        for row in imp_true_data.itertuples(index=False):
            iqs = self.prob_calc(row[:100],row[100:])
            iqs_matrix.loc[len(iqs_matrix)]=[iqs]
        return iqs_matrix['IQS']


if __name__ == "__main__":
    genotype_confusion_matrix = pd.read_csv('data/genotype_confusion_matrix.csv',sep=';',dtype=str,chunksize=14000)
    iqs_matrix = pd.DataFrame(columns=['IQS'])
    with Pool(processes=16) as pool:
        iqs = IQS()
        iqs_list = pool.map(iqs.iqs_table, genotype_confusion_matrix)
        iqs_matrix = pd.concat(iqs_list, ignore_index=True)
    iqs_matrix.to_csv('data/iqs_test.csv', sep=',', encoding='utf-8',index=False)
