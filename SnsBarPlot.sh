#!/bin/bash


if [ "$#" -ne 4 ]; then
    echo -e "This script is designed to draw the pheno distribution of a gaven SNP"
    echo -e "\nUsage: $0 VCF(str) PhenoType(str) phenotypeFile(str) SNPName(str)"
    echo -e "\nRequirements of Pip:"
    echo -e "\tmatplotlib"
    echo -e "\tseaborn"
    echo -e "\tpandas"
    exit 1
fi


vcf=$1
phe=$2
pheF=$3
snp=$4
if [[ ! -f "${snp}.${phe}.id" ]] ; then
	echo accessions > ${snp}.${phe}.id 
	head -n100 ${vcf} | grep '#CHROM' | sed 's/\t/\n/g' | awk '{if(NR>9) print}' >> ${snp}.${phe}.id
else
	echo "${snp}.${phe}.id presented, continue"
fi
if [[ ! -f "${snp}.${phe}.type" ]]; then
	echo genotypes > ${snp}.${phe}.type
	grep ${snp} ${vcf} | sed 's/\t/\n/g' | awk '{if(NR>9) print}' >> ${snp}.${phe}.type
else
	echo "${snp}.${phe}.type presented, continue"
fi
echo ${phe} > ${snp}.${phe}.phe
cat ${snp}.${phe}.id | while read i; do grep ${i} ${pheF} | cut -f2 >> ${snp}.${phe}.phe; done
paste ${snp}.${phe}.id ${snp}.${phe}.type ${snp}.${phe}.phe > ${snp}.${phe}.toplot.txt

BarPlotPhenotype.py ${snp}.${phe}.toplot.txt ${snp}.${phe}.png
