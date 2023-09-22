#!/bin/bash

#check if three arguments are provided
if [ "$#" -ne 5 ]; then
    echo -e "\033[31mUsage:\n\t\033[0m" $0 "\033[33mreference_genome(dir)\033[0m" "\033[32mquery_genome(dir)\033[0m" "\033[34mdata_type(pep/dna str)\033[0m" "\033[36mparts(int)\033[0m" "\033[35mthreads(int)\033[0m"
    echo -e "\nRequirements:\n\t""\033[33mParaFly\n\tncbi-blast\n\tsplit_FA.pl(fromTangerZhang)\033[0m"
    exit 1
fi

#assign argument values to variables
reference_genome=$1
query_genome=$2
data_type=$3
part=$4
t=$5

echo  "Splitting $query_genome into $part parts"
echo  -e "\033[32mrunning\033[0m" "perl split_FA.pl -i $query_genome -n $part"
split_FA.pl -i $query_genome -n $part

if [ "$data_type" == "pep" ] && [ "$t" -ge "$part" ]; then
    echo -e "\033[32mrunning\033[0m" '"'makeblastdb -in $reference_genome -out $reference_genome -dbtype prot'"'
    makeblastdb -in $reference_genome -out $reference_genome -dbtype prot
    echo -e "\n\n"
    echo -e "\033[32mDone, we have\033[0m"
    ls $reference_genome*
    echo -e "\n\n"
    echo -e "\033[32mNow running:\033[0m" '"'blastp -query '['All $part']'$query_genome -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastp [All]" -num_threads $t '"'
    rm blast.cmd.txt
    for i in $(seq 1 $part); do \
    cpu=$(echo "$t / $part" | bc)
    echo blastp -query $query_genome'_'$i -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastp_"$i -num_threads $cpu >> blast.cmd.txt; done
    ParaFly -c blast.cmd.txt -CPU $t
    cat $reference_genome".blastp_"* > $reference_genome".blastp"
    rm $reference_genome".blastp_"* $query_genome'_'*

elif [ "$data_type" == "dna" ] && [ "$t" -ge "$part" ]; then
    echo -e "\033[32mrunning\033[0m" '"'makeblastdb -in $reference_genome -out $reference_genome -dbtype nucl'"'
    makeblastdb -in $reference_genome -out $reference_genome -dbtype nucl
    echo -e "\n\n"
    echo -e "\033[32mDone, we have\033[0m"
    ls $reference_genome*
    echo -e "\n\n"
    echo -e "\033[32mNow running:\033[0m" '"'blastn -query '['All $part']'$query_genome -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastn [All]" -num_threads $t '"'
    rm blast.cmd.txt
    for i in $(seq 1 $part); do \
    cpu=$(echo "$t / $part" | bc)
    echo blastn -query $query_genome'_'$i -db $reference_genome -outfmt 6 -evalue 1e-5 -out $query_genome"_to_"$reference_genome".blastn_"$i -num_threads $cpu >> blast.cmd.txt; done
    ParaFly -c blast.cmd.txt -CPU $t
    cat $reference_genome".blastn_"* > $reference_genome".blastp"
    rm $reference_genome".blastn_"* $query_genome'_'*

elif [ "$t" -lt "$part" ]; then
    echo $part is smaller than $t, check your cmd!
    exit 1
else
    echo "Invalid data type. Please specify either 'pep' or 'dna'."
    exit 1
fi
