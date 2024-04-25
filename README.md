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
  
