import numpy as np
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("This script is designed to get Differential expression genes from Count Matrix")
        print("Usage python3 "+sys.argv[0]+"<Path:str> <Threshold:int>")
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


def checkZero(inl: list, threshold: int):
    n = 0
    for i in inl:
        if i > threshold:
            n += 1
    if n > 1:
        return True
    else:
        return False


path = sys.argv[1]
threshold = sys.argv[2]
hdick = {n: h for n, h in enumerate(openfile(path)[0].split('\t'))}
#######################DEG#######################
edick = {}
for i in openfile(path)[1:]:
    p = i.strip().split()
    g = p[0]
    et = []
    for ii in p[1:]:
        et.append(float(ii))
    if sum(et) == 0 or checkZero(et, int(threshold)) == False:
        continue
    else:
        e = [[np.log2(ii), n+1]for n, ii in enumerate(et)]
    edick[g] = e

Pdick = {}
Mdick = {}
for o in edick:
    ri = []
    spP = sorted(edick[o], key=lambda x: x[0], reverse=True)
    if spP[0][0] - spP[1][0] > 1:
        Pdick[o] = hdick[spP[0][1]]
    spM = sorted(edick[o], key=lambda x: x[0], reverse=False)
    if str(spM[0][0]) == '-inf':
        continue
    else:
        if spM[0][0] - spM[1][0] > -1:
            Mdick[o] = hdick[spM[0][1]]

Mdickl = [i+'\t'+Mdick[i] for i in Mdick]
Pdickl = [i+'\t'+Pdick[i] for i in Pdick]

print('We have up DEGs:', len(Mdickl))
print('We have down DEGs:', len(Pdickl))

with open('/'.join(path.split('/')[:-1]) + '.'.join(path.split('/')[-1].split('.')[0:-1]) + '.upper.E.id', 'w')as f:
    f.write('\n'.join(Pdickl))
with open('/'.join(path.split('/')[:-1]) + '.'.join(path.split('/')[-1].split('.')[0:-1]) + '.lower.E.id', 'w')as f:
    f.write('\n'.join(Mdickl))
with open('/'.join(path.split('/')[:-1]) + '.'.join(path.split('/')[-1].split('.')[0:-1]) + '.DEG.id', 'w')as f:
    f.write('\n'.join(Mdickl)+'\n'+'\n'.join(Pdickl))
