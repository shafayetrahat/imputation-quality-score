import pandas as pd
#import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input imputed file name.")
    parser.add_argument("raf", help="raf pos output file name.")
    parser.add_argument("out", help="genotype matrix output file name.")
    args = parser.parse_args()
    impute = pd.read_csv(args.input,sep=';')
    true_genotype = pd.read_csv("/data/groundtruth.csv",sep=',')
#    true_genotype = pd.read_csv("data/groundtruth_30x_test.csv",sep=',')
#    true_genotype = pd.read_csv("data/groundtruth_30x.csv",sep=',')
     #common row between true and imputed vcf
#    common = np.intersect1d(impute.POS, true_genotype.POS)
    imp_true = pd.merge(true_genotype, impute,how='inner', on=['POS','ALT','REF'])
    imp_true.dropna(inplace=True)
    pos_raf = pd.concat([imp_true['POS'],imp_true['RAF'],imp_true['REF'],imp_true['ALT']],axis = 1)
    imp_true= pd.concat([imp_true[imp_true.columns[107:]],imp_true[imp_true.columns[4:104]]],axis = 1)
    imp_true = imp_true.replace({'0/0':'1.0,0.0,0.0','0/1':'0.0,1.0,0.0','1/1':'0.0,0.0,1.0','0|0':'1.0,0.0,0.0','0|1':'0.0,1.0,0.0','1|1':'0.0,0.0,1.0'})
    imp_true.to_csv(args.out, sep=';', encoding='utf-8',index=False)
    pos_raf.to_csv(args.raf,sep=';',encoding='utf-8',index=False)
    print("Done")
