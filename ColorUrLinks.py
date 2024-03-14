import sys


def toTuple(color_str):
  components = color_str.split(',')
  r = int(components[0])
  g = int(components[1])
  b = int(components[2])
  return r, g, b


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


def fullZero(ins: str, n: int):
    return ((n - len(ins)) * '0') + ins


def middleColor(color1, color2):
  r1, g1, b1 = toTuple(color1)
  r2, g2, b2 = toTuple(color2)
  interpolated_r = (r1 + r2) // 2
  interpolated_g = (g1 + g2) // 2
  interpolated_b = (b1 + b2) // 2
  return str(interpolated_r)+','+str(interpolated_g)+','+str(interpolated_b)


if __name__ == "__main__" and len(sys.argv) < 3:
    print('Usage: python3 ' + sys.argv[0] + ' <linksFile: STR/PATH> <KaryoTypeFile: STR/PATH>')
    exit()


dick = {}
karyotype = sys.argv[2]
for i in openfile(karyotype):
    p = i.split('\t')
    dick[p[2]] = p[-1]
# colors = '223,158,212 218,137,184 213,117,157 209,96,129 204,75,102 204,75,86 211,106,89 218,137,92 225,167,95 233,198,97 205,196,101 170,186,106 134,175,110 99,165,115 70,153,120 67,136,127 65,118,135 63,100,142 61,82,150 71,74,153 90,71,153 109,69,153 127,66,153 146,64,153'

# for chr, c in zip(['Chr' + fullZero(str(i), 2) for i in range(1, 25)], colors.strip().split()):
#     dick[chr] = c
wanted = ['\t'.join(line.split('\t')[:]) + '\tcolor='+middleColor(dick[line.strip().split()[0]], dick[line.strip().split()[3]]) for line in openfile(sys.argv[1]) ]
with open("./colored.links", 'w')as f:
    f.write('\n'.join(wanted))


