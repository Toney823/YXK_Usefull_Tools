#!/bin/bash


if [ "$#" -ne 4 ]; then
    echo "Usage: $0 reference_genome(dir) query_genome(dir) data_type(pep/dnaFile) threads(int)"
    exit 1
fi

reference_genome=$1
query_genome=$2
data_type=$3
t=$4

if [ "$data_type" == "pep" ]; then
    echo -e "\033[32mrunning\033[0m" '"'makeblastdb -in $reference_genome -out $reference_genome -dbtype prot'"'
    makeblastdb -in $reference_genome -out $reference_genome -dbtype prot
    echo -e "\n\n"
    echo -e "\033[32mDone, we have\033[0m"
    ls $reference_genome*
    echo -e "\n\n"
    echo -e "\033[32mNow running:\033[0m" '"'blastp -query $query_genome -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastp" -num_threads $t '"'
    blastp -query $query_genome -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastp" -num_threads $t
elif [ "$data_type" == "dna" ]; then
    echo -e "\033[32mrunning\033[0m" '"'makeblastdb -in $reference_genome -out $reference_genome -dbtype nucl'"'
    makeblastdb -in $reference_genome -out $reference_genome -dbtype nucl
    echo -e "\n\n"
    echo -e "\033[32mDone, we have\033[0m"
    ls $reference_genome*
    echo -e "\n\n"
    echo -e "\033[32mNow running:\033[0m" '"'blastn -query $query_genome -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastn" -num_threads $t '"'
    blastn -query $query_genome -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastn" -num_threads $t
else
    echo "Invalid data type. Please specify either 'pep' or 'dna'."
    exit 1
fi
