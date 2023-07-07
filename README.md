# YXK_Usefull_Tools
A simple python package for the beginner of Bioinformatics.

faSpliter.py is a script in order to split your fasta file into multiple pieces.

ReverseComplement.py is a script to reverse part of your sequence by reversing complementary sequences.

getGFFLEN.py is a small script for building the GFF and LEN files required for WGDI usage: python3 getGFFLEN.py [gff] [whether you want mRNA or gene: mRNA/gene/CDS, anything matches your fastaID] [the abbreviation of your species] [cds.path] [pep.path]

sbatch.py also is a simple script for sbatch system job submission, srun mode and straight submission mode are supported. 
  #srun mode is only can be executed in one line
  1. echo {YOUR CMD} >> cmd.txt
  2. python3 ./sbatch.py -s cmd.txt -n {YOUR JOBS NAME} -p {NODENAMES} -c 1 -t 1 -srun(optional)
