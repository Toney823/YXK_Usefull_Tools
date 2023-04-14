import sys
import os


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


p = os.path.abspath('.')+'/'
# index = openfile(p+'index2.txt')
wantedgff = []
wantedlen = []
l1 = []
for name in sys.argv[2:]:
    file = p + name + '.gff'
    wholelen = len(list(set([c.split('\t')[0] for c in openfile(file)])))+1
    tl = [[] for _ in range(1, wholelen)]
    for line in openfile(file):
        chr = int(line.split('\t')[0])
        tl[chr-1].append('\t'.join(line.split('\t')[1:]))
    for ii in tl:
        if len(ii) == 0:
            continue
        l1.append(ii)
print(len(l1))
for n, ii in enumerate(l1):
    chr = str(n+1)
    other = sorted(ii, key=lambda x: int(x.split('\t')[4]), reverse=True)[0]
    end = other.split('\t')[2]
    geneN = other.split('\t')[4]
    wantedlen.append(chr + '\t' + end + '\t' + geneN)
    for g in ii:
        newl = chr+'\t'+g
        wantedgff.append(newl)
with open(p + sys.argv[1] + '.merged.gff', 'w')as f:
    f.write('\n'.join(wantedgff))
with open(p + sys.argv[1] + '.merged.len', 'w')as f:
    f.write('\n'.join(wantedlen))

if len(sys.argv) == 1:
    print("Usage: python " + sys.argv[0] +" outFileName FolowGffs......")
