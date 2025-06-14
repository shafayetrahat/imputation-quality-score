echo -n "CHR;POS;REF;ALT;RAF;AF;">$2
#tr '\n' ';'< data/sample_3012|sed '$ s/.$//'|sed 's/HG/imp_HG/g' >> $2
tr '\n' ';'< /samplename|sed '$ s/.$//'|sed 's/HG/imp_HG/g' >> $2
printf "\n" >> $2
bcftools query -f '%CHROM;%POS;%REF;%ALT;%RAF;%AF[;%GP]\n' $1>>$2
