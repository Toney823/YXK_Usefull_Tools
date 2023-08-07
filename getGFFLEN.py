import sys

tmpl = []
bigl = []
bigdick = {}
wantedGff = []
wantedlen = []
ingff3 = sys.argv[1]
idfer = sys.argv[2]
sn=sys.argv[3]
pep = sys.argv[4]
cds = sys.argv[5]


def changeFA(inf: str, dick: dict):
    newf = []
    for b in block_cacher_v2(openfile(inf), '>'):
        newf.append('>'+dick[b[0].replace('>', '').strip().split()[0]] + '\n' + ''.join(b[1:]))
    return newf


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


def full6(in_s: str):
    return '0'*(6-len(in_s))+in_s


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


for line1 in openfile(ingff3):
    if '#' == line1[0] or 'super' in line1[0] or 'Super' in line1[0] or 'tig' in line1[0] or 'ctg' in line1[0] or 'utg' in line1[0]:
        continue
    pool = line1.strip().split()
    if idfer in pool[2]:
        tmpl.append(pool[0])
for i in list(set(tmpl)):
    bigdick[i] = []
for line2 in openfile(ingff3):
    if '#' == line2[0] or 'super' in line2[0] or 'Super' in line2[0] or 'tig' in line2[0] or 'ctg' in line2[0] or 'utg' in line2[0]:
        continue
    pool = line2.strip().split()
    if idfer == pool[2]:
        bigdick[pool[0]].append(line2)


smallDick = {}

for n, i in enumerate(sorted(bigdick)):
    n = str(n+1)
    gn = str(len(bigdick[i]))
    wantedlen.append(n+'\t'+sorted(bigdick[i],key=lambda x: int(x.strip().split()[3]))[-1].strip().split()[4]+'\t'+str(len(bigdick[i])))
    for nn, ii in enumerate(bigdick[i]):
        nn = str(nn+1)
        col1 = n
        col2 = sn + 's' + n + 'g' + full6(nn)
        col3 = ii.strip().split()[3]
        col4 = ii.strip().split()[4]
        col5 = ii.strip().split()[6]
        col6 = nn
        col7 = ii.strip().split()[8].split(';')[0].split('=')[1]
        smallDick[col7] = col2
        wantedGff.append('\t'.join([col1, col2, col3, col4, col5, col6, col7]))
with open('.'.join(ingff3.split('.')[:-1])+'.wgdi.gff', 'w')as f:
    f.write('\n'.join(wantedGff) + '\n')
with open('.'.join(ingff3.split('.')[:-1])+'.wgdi.len', 'w')as f:
    f.write('\n'.join(wantedlen) + '\n')
with open('.'.join(pep.split('.')[:-1]) + '.wgdi.pep', 'w')as f:
    f.write('\n'.join(changeFA(pep, dick=smallDick)))
with open('.'.join(pep.split('.')[:-1]) + '.wgdi.cds', 'w')as f:
    f.write('\n'.join(changeFA(cds, dick=smallDick)))

