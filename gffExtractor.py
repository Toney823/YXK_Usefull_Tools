import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("This script is designed to extract id from gff3 file")
        print("Usage python3 "+sys.argv[0]+"<Gff:str> <IDfile:str>")
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


def gffblocker(lines: list):
    file_blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            continue
        if line.split('\t')[2] == 'gene':#startswith(separator_first):
            if len(block) > 0:
                file_blocks.append(block)
            block = [line]
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


wantedl = []
p = sys.argv[1]
id = sys.argv[2]
l = openfile(id)
for b in gffblocker(openfile(p)):
    bl = '\n'.join(b)
    for i in l:
        print(i)
        if i in bl and i not in wantedl:
            wantedl.append(bl)
        if i in bl and i in wantedl:
            continue
with open('.'.join(id.split('.')[:-1])+'.gff3', 'w')as f:
    f.write('\n'.join(wantedl))
