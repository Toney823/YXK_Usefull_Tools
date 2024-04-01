#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__" and len(sys.argv) != 5:
    print('This script is designed to get Go descriptions from genes with snps')
    print("Usage:\n\tpython3 "+ sys.argv[0] + '  <geneBed: STR>  <snpFile: STR>  <DescriptionFile: STR> <outFile: STR>\n')
    print('\tgeneBed format:')
    print('\t\t[chr: STR] <TAB> [start: INT] <TAB> [end: INT]')
    print('\tsnpFile format:')
    print('\t\t[phenotype: STR] <TAB> [snpID = (chr_pos): STR] <TAB> [pValue: FLOAT]')
    print('\tDescriptionFile format:')
    print('\t\t[gene: STR] <TAB> [description: STR]')
    exit()

def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


gene = sys.argv[1]#"./gene.bed"
snp =  sys.argv[2]#"./3_pelargonidin_3-O-beta-D-sambubi.stat"
go =  sys.argv[3]#"./f68b5fa5-c0be-4865-9f09-7f80fb8afed7.csv.description.txt"
fo = sys.argv[4]
sep = '_'
gdick = {}
for line in openfile(go):
    gdick[line.strip().split()[0].split('.')[0]] = ' '.join(line.strip().split()[1:])
# print(dick)
wantedl = []
for line in openfile(snp):
    p = line.split('\t')
    chr = p[1].split(sep)[0]
    pos = int(p[1].split(sep)[1])
    for i in openfile(gene):
        pp = i.split('\t')
        gchr = pp[0]
        gs = int(pp[1])
        ge = int(pp[2])
        g = pp[-1]
        if chr == gchr:
            if gs < pos < ge:
                if g in gdick:
                    wantedl.append(line + '\t' + g + '\t' + gdick[g])
                    print(line, g, gdick[g])
                if g not in gdick:
                    wantedl.append(line + '\t' + g + '\tNA')
                    print(line, g)
with open(fo, 'w')as f:
    f.write('\n'.join(wantedl)+'\n')
