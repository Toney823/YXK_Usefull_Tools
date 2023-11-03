#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('This script is designed to reverse complement of One || a file || \',\' separated || All DNA sequence/s')
        print("Usage:\n\tpython3 "+ sys.argv[0] + '  <DNA.fa: STR>  <seqName: STR || IdList.txt: STR || \',\' separated || 0: INT>\n')
        print("\tInstructions: \n\t\t<seqName>\tThis is a ID, if you want only one sequence get reversed and complemented\n\t\t<IdList.txt>\tThis is a file contains all of id you want to reversed and complemented\n\t\t<\',\'separated> Means you can us , separated string as input like: seq1,seq2,seq3...\n\t\t<0>\t\tMeans reverse and complement all of your fasta file.")
        print('\n\tAll <seqName> <IdList.txt> <0> are mutually exclusive.')
        exit()

fa = sys.argv[1]
name = sys.argv[2]


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


def block_cacher_v2(lines: list, separator_first: str):
    file_blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            continue
        if line.startswith(separator_first):
            if len(block) > 0:
                file_blocks.append(block)
            block = [line]
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


def rcDNA(inSeq: str):
    seqDick = {
        'A': 'T',
        'C': 'G',
        'T': 'A',
        'G': 'C',
        'N': 'N'
    }
    l = [seqDick[i] for i in inSeq[::-1]]
    return ''.join(l)


dick = {b[0][1:]: ''.join(b[1:]) for b in block_cacher_v2(openfile(fa), '>')}
wantedl = []
if name != '0' and os.path.exists(name):
    n = [n for n in openfile(name) if n in dick]
    for k in dick:
        if k not in n:
            wantedl.append('>'+k+'\n'+dick[k])
        if k in n:
            wantedl.append('>'+k+'\n'+rcDNA(dick[k]))
    with open('.'.join(fa.split('.')[:-1])+f'.{str(len(n))}Seq.reversed.fa', 'w')as f:
        f.write('\n'.join(wantedl)+'\n')
if not os.path.exists(name) and name == '0':
    for k in dick:
        wantedl.append('>'+k+'\n'+rcDNA(dick[k]))
    with open('.'.join(fa.split('.')[:-1])+'.all.reversed.fa', 'w')as f:
        f.write('\n'.join(wantedl)+'\n')
if not os.path.exists(name) and name != '0':
    for k in dick:
        if k not in name:
            wantedl.append('>' + k + '\n' + dick[k])
        if k in name:
            wantedl.append('>' + k + '\n' + rcDNA(dick[k]))
    with open('.'.join(fa.split('.')[:-1])+f'.{name}.reversed.fa', 'w')as f:
        f.write('\n'.join(wantedl)+'\n')
if ',' in name and len(name.split(',')) >= 2:
    namel = name.split(',')
    for k in dick:
        if k not in namel:
            wantedl.append('>' + k + '\n' + dick[k])
        if k in namel:
            wantedl.append('>' + k + '\n' + rcDNA(dick[k]))
    with open('.'.join(fa.split('.')[:-1])+f'.{len(namel)}Seq.reversed.fa', 'w')as f:
        f.write('\n'.join(wantedl)+'\n')
elif not os.path.exists(name) and name != '0' and name not in dick:
    print('Input Error Check Your Data!')
