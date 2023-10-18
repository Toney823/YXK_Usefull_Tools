#!/usr/bin/env python3
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as psl
import pandas as pd
import sys
matplotlib.use('Agg')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("This script is designed to draw the phenotype distribution of gaven genotype")
        print("Usage:\n\tpython3 "+sys.argv[0]+" <Matrix:str> <outPlot>\n")
        print('Matrix format:\n\t')
        print('\taccessions	genotypes(Requirement)	PhenotypeName(youNameIt)\n'
'\tDP8450004549TL_L01_394	1/1	31611490.52\n'
'\tDP8450004535BR_L01_369	1/1	20556221.41\n'
'\tDP8450004554TL_L01_397	0/1	13659022.69\n'
'\tDP8450004554TL_L01_400	0/1	122043935.8\n'
'\tDP8450004534BR_L01_339	0/1	6887900.343\n'
'\tDP8450004554TL_L01_405	0/1	21462903.9\n'
'\tDP8450004555TL_L01_408	0/1	10271531.2\n')
        exit()

inf = sys.argv[1]
ouf = sys.argv[2]
df = pd.read_table(inf)
df.head()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
psl.use('ggplot')
plt.figure(figsize=(18, 12))
sns.boxplot(x=df['genotypes'],y=df.columns[2],data=df)#.savefig(ouf)
fig1 = plt.gcf()
fig1.savefig(ouf)

