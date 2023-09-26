import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from met_brewer import met_brew
import os
import sys
# if __name__ == "__main__":
#     if len(sys.argv) < 4:
#         print("This script can take multiple ONELINE ")
#         print("Usage python3 "+sys.argv[0]+" <Dir: STR> <OrderFile:STR> <Tone:STR> <ExhibitionLimit: INT> <savetype: STR>")
#         exit()
###########以下为参数部分###########
dir = r"E:\test"#年份文件存放文件夹的路径
order = r"E:\test\order.txt"#展示顺序
tone = "Wissing" #https://github.com/BlakeRMills/MetBrewer#colorblind-friendly-checking 找一个喜欢的画家风格
lower = 0#展示下限
upper = 10#展示上限
# save = 'png'
'''
Requirements:
    pip install met_brewer
    pip install seaborn
    pip install pands
    pip install matplotlib
'''
###########以下为绘图部分###########
sns.set(color_codes=True)
plt.rcParams['figure.facecolor'] = 'none'
plt.rcParams['axes.facecolor'] = 'none'


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


def colorSelecting(tone: str, number: int):
  t = []
  def hex_to_rgb(hex_color):
    if hex_color.startswith("#"):
      hex_color = hex_color[1:]
    if len(hex_color) not in (3, 6):
      raise ValueError("Invalid hex color: " + hex_color)
    if len(hex_color) == 3:
      hex_color = "".join(c * 2 for c in hex_color)
    red_hex = hex_color[:2]
    green_hex = hex_color[2:4]
    blue_hex = hex_color[4:]
    red = str(int(red_hex, 16))
    green = str(int(green_hex, 16))
    blue = str(int(blue_hex, 16))
    return (red, green, blue)

  for i in met_brew(name=tone, n=number, brew_type="continuous"):
    c = list(hex_to_rgb(i))
    result = [','.join(c[ii:ii+3]) for ii in range(0, len(c), 3)][0]
    t.append(tuple(result.split(',')))
  return t


def snsRGB(inc):
    return tuple(int(x)/255 for x in inc)


c = 0
fig, ax = plt.subplots(figsize=(8, 12), zorder=0)
dick = {}
for i in openfile(order):
    for f in os.listdir(dir):
        if i in f and i == f.split('.')[0]:
            dick[dir + '\\' + f] = f
            # dick[dir + '//' + f] = f


for color, fi in zip(colorSelecting(tone=tone, number=len(dick)), dick.keys()):
    c += 1
    a = len(dick)
    axf = fig.add_subplot(a, 1, c, sharex=ax)
    axf.set_ylabel(dick[fi].split('.')[0], fontdict={'size': 10}, rotation=0, labelpad=len(dick[fi].split('.')[0])*6)
    axf.set_xlabel(None)
    axf.set_yticks([])
    df = pd.read_table(fi, header=None).squeeze()
    data = df / 1e6
    readD = data[(data > lower) & (data < upper)]
    if c != len(dick):
        axf.tick_params('x', labelbottom=False)
        sns.kdeplot(data=readD, fill=True, ax=axf, zorder=1, color=snsRGB(color))
    sns.kdeplot(data=readD, fill=True, ax=axf, zorder=1, color=snsRGB(color))
plt.xlabel('Mya')
plt.tight_layout()
plt.xlim(0)
ax.set_yticklabels([])
plt.show()
# plt.savefig('KS.'+ save, format=save, bbox_inches='tight', dpi=300, transparent=True)
