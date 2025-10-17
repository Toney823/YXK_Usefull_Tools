# YXK_Usefull_Tools
## Dependence
### python-docx
### jieba
### numpy
### scipy
### met_brewer
### Pandas
    
A simple Python package and some simple scripts for the beginner of Bioinformatics.

# faSpliter.py

#### faSpliter.py is a script in order to split your fasta file into multiple pieces.
 
# ReverseComplement.py
#### ReverseComplement.py is a script to reverse part of your sequence by reversing complementary sequences.

# getGFFLEN.py
getGFFLEN.py is a small script for building the GFF and LEN files required for WGDI 
 
usage:
 	
	python3 getGFFLEN.py [gff] [whether you want mRNA or gene: mRNA/gene/CDS, anything matches your fastaID] [the abbreviation of your species] [cds.path] [pep.path]
 
# sbatch.py
	sbatch.py also is a simple script for sbatch system job submission, srun mode and straight submission mode are supported.   
#### srun mode is only can be executed in one line  
#### 1. 
	echo {YOUR CMD} >> cmd.txt  
#### 2. 
	python3 ./sbatch.py -s cmd.txt -n {YOUR JOBS NAME} -p {NODENAMES} -c 1 -t 1 -srun(yes or no REQUIRED) -y (yes or [EMPTY] OPTIONAL)  
  
# diploidGffRenamder.py is a simple script for organizing your gff3 file  

	python ./Gff3Renamer.py <GFF3: STR/PATH> <ABBREVIATION: STR> <CONTIGMARKER: STR> <PEP: STR> <CDS: STR> <GENE: STR>  
 
# plinkSNP2fasta.py
plinkSNP2fasta.py extracts SNPs information from VCF and chromosomes fasta, generating multiple chromosomes fasta files based on your sample numbers.  

	python3 plinkSNP2fasta.py <CHR_FASTA> <SNP_VCF> <OUTDIR>  

# parablast.sh
parablast.sh is a simple script that runs blast in parallel mod

 	bash parablast.sh reference_genome(dir) query_genome(dir) data_type(pep/dna str) parts(int) threads(int)  
## Requirements are: 
 ### ParaFly,  

 ### ncbi-blast  
and 
 ### split_FA.pl (Which is from TangerZhang, you can find this script in YXK_Usefull_Tools) 

 # faRC.py
 A simple script for DNA sequences reverse and complement
 #### python3 faRC.py <DNA.fa: STR>  <seqName: STR || IdList.txt: STR || 0: INT>
 	Instructions: 
		<seqName>		This is an ID, if you want only one sequence get reversed and complemented
		<IdList.txt>	This is a file containing all of the id you want to reverse and complement
		<0>				Means reverse and complement all of your fasta files.
[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/Toney823/YXK_Usefull_Tools)
