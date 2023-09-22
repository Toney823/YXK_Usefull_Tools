#!/usr/bin/perl -w
use Getopt::Std;
getopts "i:n:";
if( (!defined $opt_i) or (!defined $opt_n) ){
	die "**********************************************
	This script was used to split big fasta data into small fasta data set
	Usage: perl split_FA.pl -i fasta_file -n number_of_parts
	   -i: the input fasta file
	   -n: how many parts you want to split
	   -h: help and usage
**********************************************\n";
	}
###This script was used to split big fastq data into small fq data set###
###usage: perl split_FQ.pl fq_file number_of_parts###


$n_part = $opt_n;
$fq_file = $opt_i;
$total_reads = 0;

open(IN, $fq_file) or die"";
$/='>';
<IN>;
while(<IN>){
	chomp;
	($gene,$seq) = split(/\n/,$_,2);
	$gene =~ s/\s+.*//g;
	$seq  =~ s/\s+//g;
	$total_reads++;
	$infordb{$total_reads} = ">".$gene."\n".$seq."\n";
	}
close IN;

$part_reads = int ($total_reads/$n_part);
$n = 0;
for($i=1;$i<=$total_reads;$i=$i+$part_reads){
	$n++;
	$output = $fq_file."_".$n;
	open($fh, "> $output") or die"";
	if($n == $n_part){
	 for($j=$i;$j<=$total_reads;$j++){
	  	print $fh "$infordb{$j}";
		 }
		last;
		}else{
    	for($j=$i;$j<$i+$part_reads;$j++){
    		print $fh "$infordb{$j}";
    		}			
			}
	close $fh;
	}
