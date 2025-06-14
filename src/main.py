import subprocess
import argparse
import re
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #vcf-to-csv
    parser.add_argument("input", help ="genotype matrix input file")
    parser.add_argument("output", help ="output csv file")
    args = parser.parse_args()
    smpl_num = re.findall(r'\d+',str(args.input))
#    sample_imp = '/data/imputed-'+smpl_num[0]+'.csv'
    raf_pos = './raf-pos-'+smpl_num[0]+'.csv'
    conf_mat =args.input
    cor_mat = './pearson-'+smpl_num[0]+'.csv'
#    print("Running...\n",'./vcf-to-csv.sh '+args.input+" "+sample_imp)
#    subprocess.run(['bash','/vcf-to-csv.sh',args.input,sample_imp])
#    print("vcf to csv conversion is done")
#    print("Running...\n python merge_matrix.py",sample_imp,raf_pos,conf_mat)
#    subprocess.run(['python', '/merge_matrix.py',sample_imp,raf_pos,conf_mat])
#    print("merging done")
    print("Running...\n pearson.py")
    print('python','pearson.py',conf_mat,cor_mat)
    subprocess.run(['python','/pearson.py',conf_mat,cor_mat])
    print("Generate Quartile deviation and Median....")
    subprocess.run(['python','/plot-pearson-quartile-deviation.py',cor_mat,raf_pos,args.output])
    print("All job done")
