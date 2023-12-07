import sys


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("This script is designed twist the bed file by chromosomes required by JCVI")
        print("Usage:\n\tpython3 "+sys.argv[0]+" <inbed:STR--Old JCVI`s bed> <outbed:STR--New JCVI`s bed> <ChrList:STR--Chromosomes you want to twist>")
        exit()


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    f_open.close()
    return lines


def bed2Dick(inbed: str):
    print('Generating jcvi bed directory')
    # l = []
    ld = {}
    for i in openfile(inbed):
        pool = i.split('\t')
        if pool[0] not in ld:
            ld[pool[0]] = {}
            ld[pool[0]][pool[3]] = [int(pool[1]), int(pool[2]), int(pool[2])-int(pool[1]), pool[3], pool[4], pool[5]]
        if pool[0] in ld:
            ld[pool[0]][pool[3]] = [int(pool[1]), int(pool[2]), int(pool[2])-int(pool[1]), pool[3], pool[4], pool[5]]
    print('Done generating')
    return ld


fin = sys.argv[1]#r"E:\LW\XZWJ\line3.bed"
fo =sys.argv[2]#r"E:\LW\XZWJ\line3.tested.bed"
toDoChr = openfile(sys.argv[3])#['pbsqHic_asm_6', 'pbsqHic_asm_1']


orientDick={"+": "-", "-": "+"}
allL = []
d = bed2Dick(fin)
for chr in d:
    if chr in toDoChr:
        print(chr, 'is what you want')
        ll = sorted(d[chr].values(), key=lambda x: x[0])[-1][1]+1
        print(chr, 'started twisting','\n')
        wangedl = []
        for gene in list(d[chr])[::-1]:
            info = d[chr][gene]
            oldS = info[0]
            gLen = info[2]
            newS = ll-oldS
            newE = newS-gLen
            allL.append('\t'.join([chr, str(newE), str(newS), gene, info[4], orientDick[info[5]]]))
        print('Done')
    else:
        print(chr, 'is not what you want')
        for gene in list(d[chr]):
            info = d[chr][gene]
            oldS = info[0]
            gLen = info[2]
            oldE = oldS + gLen
            allL.append('\t'.join([chr, str(oldS), str(oldE), gene, info[4], info[5]]))
with open(fo, 'w')as f:
    f.write('\n'.join(allL)+'\n')
