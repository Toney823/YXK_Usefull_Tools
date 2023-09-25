#!/bin/bash

if [ "$#" -ne 5 ]; then
    echo -e "\033[31mUsage:\n\t\033[0m$0 \033[33mreference_genome(dir)\033[0m \033[32mquery_genome(dir)\033[0m \033[34mdata_type(pep/dna str)\033[0m \033[36mparts(int)\033[0m \033[35mthreads(int)\033[0m"
    echo -e "\nRequirements:\n\t\033[33mParaFly\n\tncbi-blast\n\tsplit_FA.pl(fromTangerZhang)\033[0m"
    exit 1
fi

reference_genome="$1"
query_genome="$2"
data_type="$3"
part="$4"
t="$5"

if [ "$t" -lt "$part" ]; then
    echo -e "\033[31m$part parts can not be splited into $t CPUs, check your arguments!\033[0m"
    echo -e "\033[0m$0 \033[33mreference_genome(dir)\033[0m \033[32mquery_genome(dir)\033[0m \033[34mdata_type(pep/dna str)\033[0m \033[36mparts(int)\033[0m \033[35mthreads(int)\033[0m"
    exit 1
fi

echo -e "\033[32mSplitting $query_genome into $part parts\033[0m"
echo -e "\033[32mrunning\033[0m perl split_FA.pl -i $query_genome -n $part"
perl split_FA.pl -i "$query_genome" -n "$part"

if [ "$data_type" == "pep" ] && [ "$t" -ge "$part" ]; then
    if [ ! -f "${reference_genome}.psq" ] || [ ! -f "${reference_genome}.pin" ] || [ ! -f "${reference_genome}.phr" ] || [ ! -f "${reference_genome}.pdb" ] || [ ! -f "${reference_genome}.pto" ] || [ ! -f "${reference_genome}.pot" ] || [ ! -f "${reference_genome}.ptf" ]; then
    echo -e "\033[32mrunning\033[0m makeblastdb -in $reference_genome -out $reference_genome -dbtype prot"
    makeblastdb -in "$reference_genome" -out "$reference_genome" -dbtype prot
    echo -e "\n\n"
    echo -e "\033[32mDone, we have\033[0m"
    ls "${reference_genome}"*
    echo -e "\n\n"
    else
        echo -e "\033[32mReference database already exists. No need to recreate it.\033[0m "
    fi
    echo -e "\033[32mNow running:\033[0m blastp -query '[All $part]$query_genome' -db $reference_genome -outfmt 6 -evalue 1e-5 -out ${query_genome}_to_${reference_genome}.blastp [All] -num_threads $t"
    for i in $(seq 1 "$part"); do
        cpu=$(echo "$t / $part" | bc)
        echo "blastp -query ${query_genome}_${i} -db $reference_genome -outfmt 6 -evalue 1e-5 -out ${query_genome}_to_${reference_genome}.blastp_${i} -num_threads $cpu"; done > blast.cmd.sh
    if  [ -f "blast.cmd.sh.completed" ]; then
        rm blast.cmd.sh.completed
    else
        echo -e '\033[32mRunning First time, no ParaFly output\033[0m'
    fi
    ParaFly -c blast.cmd.sh -CPU "$t"
    cat ${query_genome}_to_"${reference_genome}.blastp_"* > ${query_genome}_to_"${reference_genome}.blastp"
    for i in $(seq 1 "$part"); do
	  rm ${query_genome}_to_"${reference_genome}.blastp_"${i} && rm "${query_genome}"_${i}; done
    rm blast.cmd.sh.completed

elif [ "$data_type" == "dna" ] && [ "$t" -ge "$part" ]; then
    if [ ! -f "${reference_genome}.psq" ] || [ ! -f "${reference_genome}.pin" ] || [ ! -f "${reference_genome}.phr" ] || [ ! -f "${reference_genome}.pdb" ] || [ ! -f "${reference_genome}.pto" ] || [ ! -f "${reference_genome}.pot" ] || [ ! -f "${reference_genome}.ptf" ]; then
    echo -e "\033[32mrunning\033[0m makeblastdb -in $reference_genome -out $reference_genome -dbtype nucl"
    makeblastdb -in "$reference_genome" -out "$reference_genome" -dbtype nucl
    echo -e "\n\n"
    echo -e "\033[32mDone, we have\033[0m"
    ls "${reference_genome}"*
    echo -e "\n\n"
    else
        echo -e "\033[32mReference database already exists. No need to recreate it.\033[0m"
    fi
    echo -e "\033[32mNow running:\033[0m blastn -query '[All $part]$query_genome' -db $reference_genome -outfmt 6 -evalue 1e-5 -out ${query_genome}_to_${reference_genome}.blastn [All] -num_threads $t"
    for i in $(seq 1 "$part"); do
        cpu=$(echo "$t / $part" | bc)
        echo "blastn -query ${query_genome}_${i} -db $reference_genome -outfmt 6 -evalue 1e-5 -out ${query_genome}_to_${reference_genome}.blastn_${i} -num_threads $cpu"; done > blast.cmd.sh
    if  [ -f "blast.cmd.sh.completed" ]; then
        rm blast.cmd.sh.completed
    else
        echo -e '\033[32mRunning First time, no ParaFly output\033[0m'
    fi
    ParaFly -c blast.cmd.sh -CPU "$t"
    cat ${query_genome}_to_"${reference_genome}.blastn_"* > ${query_genome}_to_"${reference_genome}.blastn"
    for i in $(seq 1 "$part"); do
	  rm ${query_genome}_to_"${reference_genome}.blastn_"${i} && rm "${query_genome}"_${i}; done
    rm blast.cmd.sh.completed
else
    echo -e "\033[31mInvalid data type. Please specify either 'pep' or 'dna'.\033[0m"
    exit 1
fi
