# YXK_Usefull_Tools
A simple python package for the beginner of Bioinformatics.

faSpliter.py is a script in order to split your fasta file in to mutiple pieces.

ReverseComplement.py is a script to reverse part of your sequence by reversing complementary sequences.

getGFFLEN.py is a small script for building the GFF and LEN files required for WGDI usage: python3 getGFFLEN.py [gff] [whether you want mRNA or gene: mRNA/gene/CDS, anything match your fastaID] [the abbreviation of your species] [cds.path] [pep.path]

sbatch.py also is a simple script for sbatch system job submission, srun mode and straight submission mode are supported. 
  1. echo {YOUR CMD} >> cmd.txt
  2. python3 ./sbatch.py -s cmd.txt -n plinkFilter -p low -c 1 -t 1
