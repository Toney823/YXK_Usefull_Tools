#!/usr/bin/python3
import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('This script is designed to insert intron region into gff3 file.')
        print('Usage: python3 ' + sys.argv[0] + ' <inGFF3: STR/PATH> ')
        sys.exit()


f = sys.argv[1]


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


def gffblocker(lines: list):
    file_blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            continue
        if line.split('\t')[2] == 'gene':
            if len(block) > 0:
                file_blocks.append(block)
            block = [line]
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


for b in gffblocker(openfile(f)):
    newb = []
    tmpL = []
    geneInfo = b[0].strip().split()
    gene = b[0].strip().split()[-1].split(';')[0].split('=')[1]
    n = 0
    l = []
    mrna = None
    for line in b:
        p = line.strip().split()
        if p[2] == 'intron':
            print('Your gff3 file has already inserted with intron. Skip this step.')
            exit()
        if p[2] == 'mRNA':
            mrna = line.strip().split('\t')[-1].split(';')[0].split('=')[1]
        if p[2] == 'gene':
            l = [gene.replace('gene:', ''), p[0], p[3], p[4], p[6]]
        elif p[2] == 'exon':
            l.append(p[3])
            l.append(p[4])
        else:
            continue
    tmpLenth = len(l)
    namel = []
    if tmpLenth > 7:
        for i in range(7, tmpLenth, 2):
            nn = str(n+1)
            intronE = int(l[i]) - 1
            intronS = int(l[i - 1]) + 1
            intronLine = '\t'.join([l[1], 'Python', 'intron', str(intronS), str(intronE), '0', l[4], 'ID=intron:'+l[0]+'.intron.'+nn+';Parent=' + mrna])
            b.append(intronLine)
            n+=1
    if tmpLenth == 7:
        pass
    print('###')
    [print(_) for _ in sorted(b, key=lambda x: int(x.split('\t')[3]))]
