import pandas as pd
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input imputed file name.")
    parser.add_argument("raf", help="raf pos output prefix. Format: <raf><chunk_number>.csv")
    parser.add_argument("out", help="genotype matrix output prefix. Format: <out><chunk_number>.csv")
    args = parser.parse_args()
    source_path = args.input
    ground_source_path = "/groundtruth.csv"
    true_genotype = pd.read_csv(ground_source_path,sep=',')
    for i,impute in enumerate(pd.read_csv(source_path, sep=';', chunksize=10000)):
        imp_true = pd.merge(true_genotype, impute,how='inner', on=['POS','ALT','REF'])
        imp_true.dropna(inplace=True)
        pos_raf = pd.concat([imp_true['POS'],imp_true['RAF'],imp_true['REF'],imp_true['ALT']],axis = 1)
        imp_true= pd.concat([imp_true[imp_true.columns[107:]],imp_true[imp_true.columns[4:104]]],axis = 1)
        imp_true = imp_true.replace({'0/0':'1.0,0.0,0.0','0/1':'0.0,1.0,0.0','1/1':'0.0,0.0,1.0','0|0':'1.0,0.0,0.0','0|1':'0.0,1.0,0.0','1|1':'0.0,0.0,1.0'})
        imp_true_filename = args.out+str(i)+'.csv'
        pos_raf_filename = args.raf+str(i)+'.csv'
        imp_true.to_csv(imp_true_filename, sep=';', encoding='utf-8',index=False)
        pos_raf.to_csv(pos_raf_filename,sep=';',encoding='utf-8',index=False)
        print(i,"iter is done.")
