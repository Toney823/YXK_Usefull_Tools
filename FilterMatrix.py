import sys
import numpy as np
import scipy.stats as stats


if __name__ == "__main__" and len(sys.argv) < 2:
    print('Usage: python3 ' + sys.argv[
        0] + ' <Your expression matrix: STR 我们默认将前三列为参考列，后三列为处理列>')
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



file = sys.argv[1]#r"F:\sn\15a1-4.fpkm.txt"
dick = {}
Z2O = []
O2Z = []
epsilon = 1e-10
Up = []
Down = []
fcUp = []
fcDown = []

for n, line in enumerate(openfile(file)):
    p = line.strip().split('\t')
    if n == 0:
        dick = {n: header for n, header in enumerate(p)}
    if len(p) == 0:
        continue
    if n > 0 and len(p) > 0:
        l = [p[0]]
        for i in p[1:]:
            l.append(float(i))
        ctl = l[1:4]
        trt = l[4:]
        ctlSum = sum(ctl)
        trtSum = sum(trt)
        ctlAve = np.average(ctl)
        trtAve = np.average(trt)
        AveRrtTTest = stats.ttest_ind(ctl, trt, equal_var=False)[1]

        l.append(ctlAve)
        l.append(trtAve)
        l.append(ctlSum)
        l.append(trtSum)
        l.append(AveRrtTTest)

        if AveRrtTTest > 0.05 or ctlSum < 1 and trtSum < 1:
            continue
        elif ctlSum == 0 and trtSum != 0:
            Z2O.append(l)
        elif trtSum == 0 and ctlSum != 0:
            O2Z.append(l)
        else:
            log2fc = np.log2(trtAve / ctlAve)
            l.append(log2fc)

            if log2fc > 1:
                fcUp.append(l)
            elif log2fc > 0:
                Up.append(l)

            if log2fc < -1:
                fcDown.append(l)
            elif log2fc < 0:
                Down.append(l)


header = list(dick.values()) + ['ctlAverage', 'treatAverage', 'ctlSum', 'treatSum', 'Pvalue', 'Log2FC']
lll = []

def fuckList(inList: list):
    return ['\t'.join(map(str, line)) for line in inList]

for name, ii in zip(['Up', '2fcUp', 'Down', '2fcDown', 'Zero2N', 'N2Zero'], [Up, fcUp, Down, fcDown, Z2O, O2Z]):
    ii.insert(0, header)
    with open('.'.join(file.split('.')[:-1])+'.'+name+'.txt', 'w')as f:
        f.write('\n'.join(fuckList(ii)))
