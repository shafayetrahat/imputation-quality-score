import pandas as pd
#import numpy as np
from scipy import stats
from multiprocessing import Pool
import argparse

class Pearson:
    def __init__(self):
        pass

    def prob_calc(self, imp_data,true_data ):
        count =0.0
        tmp =0.0
        for i in range(len(imp_data)):
            if true_data[i] =='./.' or true_data[i] == '.|.':
                continue
            else:
                imp_val = [float(x) for x in imp_data[i].split(',')]
                true_val = [float (x) for x in true_data[i].split(',')]
                tmp = tmp + stats.pearsonr(imp_val,true_val)[0]
                count = count+1.0
            pcor = tmp/count
        return pcor


    def pearson_table(self,imp_true_data):
        '''This function will genereate pearson martix for the whole vcf'''
        pearson_matrix = pd.DataFrame(columns=['PCOR'])
        count =0
        for row in imp_true_data.itertuples(index=False):
            pearson = self.prob_calc(row[:100],row[100:])
            pearson_matrix.loc[len(pearson_matrix)]=[pearson]
        return pearson_matrix['PCOR']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input genotype confusion matrix file")
    parser.add_argument("out", help="output file")
    args = parser.parse_args()
    genotype_confusion_matrix = pd.read_csv(args.input,sep=';',chunksize=14000)
    pearson_matrix = pd.DataFrame(columns=['PCOR'])
    with Pool(processes=1) as pool:
        pearson = Pearson()
        pearson_list = pool.map(pearson.pearson_table, genotype_confusion_matrix)
        pearson_matrix = pd.concat(pearson_list, ignore_index=True)
    pearson_matrix.to_csv(args.out, sep=',', encoding='utf-8',index=False)
