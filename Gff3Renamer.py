#!/usr/bin/env python3
import sys


if __name__ == "__main__" and len(sys.argv) < 5:
    print('Usage: python3 ' + sys.argv[
        0] + ' <GFF3: STR/PATH> <ABBREVIATION: STR> <CONTIGMARKER: STR> <GENOME: STR>')
    # print('Usage: python3 ' + sys.argv[0] + ' <GFF3: STR/PATH> <ABBREVIATION: STR> <CONTIGMARKER: STR> <PEP: STR> <CDS: STR> <GENE: STR> <GENOME: STR>')
    exit()

og = sys.argv[1]
abrev = sys.argv[2]
tigMarker = sys.argv[3]
# pep = sys.argv[4]
# cds = sys.argv[5]
# genef = sys.argv[6]
genome = sys.argv[4]
dick = {}


def openGff(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0:
            continue
        lines.append(line)
    return lines


def fullZero(ins: str, n: int):
    return ((n - len(ins)) * '0') + ins


def block_cacher(lines: list, separator_first: str):
    file_blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == separator_first:
            if len(block) > 0:
                file_blocks.append(block)
            block = []
            block.append(line)
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


for b in block_cacher(openGff(og), '#'):
    if len(b) < 2:
        continue
    chr = b[1].strip().split()[0]
    if chr in dick:
       dick[chr].append(b[1:])
    elif not chr in dick:
        dick[chr] = [b[1:]]


def faRenamer(infa: list, d: dict):
    newf = []
    for b in infa:
        n = b[0][1:]
        for i in d:
            if i in n or n in i or n == i:
                newf.append('>' + d[i] + '\n' + ''.join(b[1:]))
    return newf


wantedGff = ['###GFF3FORMAT']
nn = 0
tigN = 0
nameDick = {}
chrDick = {}
for k in dick.keys():
    if k.startswith('Chr'):
        chrDick[k] = k
        for n, block in enumerate(sorted(dick[k], key=lambda x: int(x[0].strip().split()[3]))):
            gene = block[0].strip().split()[-1].split(';')[0].split('=')[1]
            newName = abrev + k.replace('Chr', '') + 'G' + fullZero(str(n+1), 6) + '0'
            wantedGff.append('\n'.join(block).replace(gene, newName)+'\n###')
            nameDick[gene] = newName
    if tigMarker in k:
        tigN += 1
        tigName = abrev + 'Contig' + fullZero(str(tigN), 6)
        chrDick[k] = tigName
        for n, block in enumerate(sorted(dick[k], key=lambda x: int(x[0].strip().split()[3]))):
            nn += 1
            gene = block[0].strip().split()[-1].split(';')[0].split('=')[1]
            newName = abrev + str(nn) + 'T' + fullZero(str(n+1), 6) + '0'
            wantedGff.append('\n'.join(block).replace(gene, newName).replace(k, tigName)+'\n###')
            nameDick[gene] = newName
with open('.'.join(og.split('.')[:-1]) + '.' + abrev + '.gff3', 'w')as f:
    f.write('\n'.join(wantedGff))
with open('.'.join(og.split('.')[:-1]) + '.' + abrev + '.genome.fasta', 'w')as f:
    f.write('\n'.join(faRenamer(infa=block_cacher(openGff(genome), '>'), d=chrDick))+'\n')
# with open('.'.join(og.split('.')[:-1]) + '.' + abrev + '.pep', 'w')as f:
#     f.write('\n'.join(faRenamer(infa=block_cacher(openGff(pep), '>'), d=nameDick))+'\n')
# with open('.'.join(og.split('.')[:-1]) + '.' + abrev + '.cds', 'w')as f:
#     f.write('\n'.join(faRenamer(infa=block_cacher(openGff(cds), '>'), d=nameDick))+'\n')
# with open('.'.join(og.split('.')[:-1]) + '.' + abrev + '.gene', 'w')as f:
#     f.write('\n'.join(faRenamer(infa=block_cacher(openGff(genef), '>'), d=nameDick))+'\n')
