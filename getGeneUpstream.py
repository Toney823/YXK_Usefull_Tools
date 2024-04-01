#!/usr/bin/env python3
import sys


if __name__ == "__main__" and len(sys.argv) != 4:
    print('This script is designed to get the extract the upper region from bed file of gff3')
    print("Usage:\n\tpython3 "+ sys.argv[0] + '  <geneBed: STR> <outFile: STR> <length: INT>')
    print("\tgeneBed: BED file of gene:\t[chr: STR] <TAB> [start: INT] <TAB> [end: INT] <TAB> [gene:STR]")
    print("\tAttention: \n\t\tWhile I am extracting the upper region of genes, if the length you`re trying to extract is\n"
          "\t\tlonger than the Inter-Genetic Region(IGR), I`ll use the IGR instead.")
    exit()


inBed = sys.argv[1]#r"E:\LW\gwas\toStat.bed"
outBed = sys.argv[2]#'E:\LW\gwas\test.out.txt'
length = int(sys.argv[3])#5000
d = {}


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


for i in openfile(inBed):
    if i.split('\t')[0] not in d:
        d[i.split('\t')[0]] = [i]
    elif i.split('\t')[0] in d:
        d[i.split('\t')[0]].append(i)

wantedl = []
for chr in d:
    pool = d[chr]
    for n, line in enumerate(pool):
        p = line.split('\t')
        start = int(p[1])
        end = int(p[2])
        orient = p[3]
        gene = p[4]
        if n == 0 and orient == '+' and start >= length:
            newStart = start - length
            newEnd = start
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n == 0 and orient == '+' and start < length:
            newStart = 0
            newEnd = start
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n == 0 and orient == '-' and int(pool[n + 1].split('\t')[1]) - end < length:
            newStart = end
            newEnd = int(pool[n + 1].split('\t')[1])
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n == 0 and orient == '-' and int(pool[n + 1].split('\t')[1]) - end >= length:
            newStart = end
            newEnd = end + length
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n != 0 and n != len(pool)-1 and orient == '+' and start - int(pool[n - 1].split('\t')[2]) >= length:
            newStart = start - length
            newEnd = start
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n != 0 and n != len(pool)-1 and orient == '+' and start - int(pool[n - 1].split('\t')[2]) < length:
            newStart = int(pool[n - 1].split('\t')[2])
            newEnd = start
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n != 0 and n != len(pool)-1 and orient == '-' and int(pool[n + 1].split('\t')[1]) - end >= length:
            newStart = end
            newEnd = end + length
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n != 0 and n != len(pool)-1 and orient == '-' and int(pool[n + 1].split('\t')[1]) - end < length:
            newStart = end
            newEnd = int(pool[n + 1].split('\t')[1])
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n == len(pool)-1 and orient == '+' and start - int(pool[n - 1].split('\t')[2]) >= length:
            newStart = start - length
            newEnd = start
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n == len(pool)-1 and orient == '+' and start - int(pool[n - 1].split('\t')[2]) < length:
            newStart = int(pool[n - 1].split('\t')[2])
            newEnd = start
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)
        if n == len(pool)-1 and orient == '-':
            newStart = end - length
            newEnd = end
            wantedl.append(str(chr) + "\t" + str(newStart) + "\t" + str(newEnd) + "\t" + gene)

with open(outBed, 'w')as f:
    f.write('\n'.join(wantedl))
