import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("This script is designed to get representative population from the Q matrix from admixture")
        print("The file should looks like this:")
        print('FP150000610(AccessionID)	0.1148	0.0261	0.4931	0.3659  ...  ...  ...')
        print('           ...            ...      ...     ...    ...    ...  ...  ...')
        print('           ...            ...      ...     ...    ...    ...  ...  ...')
        print("Usage python3 "+sys.argv[0]+" <MatrixFile:str> <Threshold:float - 0~1>")
        exit()

f = sys.argv[1]#"E:\LW\gwas\204\tofilte.txt"
filter = sys.argv[2]#0.5


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


dick = {}
for i in openfile(f):
    p = i.strip().split()
    dick[p[0]] = {}
    for n, ii in enumerate(p[1:]):
        dick[p[0]][ii] = n+1
outDick = {}
for k in dick:
    biggest = float(sorted(dick[k], key=lambda x: float(x), reverse=True)[0])
    number = dick[k][sorted(dick[k], key=lambda x: float(x), reverse=True)[0]]
    if biggest > float(filter):
        if number not in outDick:
            outDick[number] = []
            outDick[number].append(k)
        elif number in outDick:
            outDick[number].append(k)
count = []
for cat in outDick:
    with open('.'.join(f.split('.')[:-1]) + '.columNumber'+str(cat)+'.'+str(filter*100)+'.id', 'w')as f:
        f.write('\n'.join(outDick[cat]))
    count.append(len(outDick[cat]))
    print('We have', len(outDick[cat]), 'accessions with highest proportion bigger than', str(filter*100)+'%', 'located in colum number', cat)
print(sum(count))

