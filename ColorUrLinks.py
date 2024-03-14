#!/usr/bin/python3
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

wanted = ['\t'.join(line.split('\t')[:]) + '\tcolor='+middleColor(dick[line.strip().split()[0]], dick[line.strip().split()[3]]) for line in openfile(sys.argv[1]) ]
with open("./colored.links", 'w')as f:
    f.write('\n'.join(wanted))


