#!/usr/bin/python3
import gzip
import sys

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Notice: This script is to convert vcf file of SNPs into chromosomes specially for the vcfs after the "
              "FUCKING PLINK filted!!!!")
        print("Usage python3 "+sys.argv[0]+" <CHR_FASTA> <SNP_VCF> <OUTDIR>")
        exit()

ing = sys.argv[1]
inv = sys.argv[2]
oD = sys.argv[3]


def block_cacher(lines: list, separator_first: str):
    file_blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == separator_first:
            if len(block) > 0:
                file_blocks.append(block)
            block = []
            block.append(line)
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


class openfile_V2:

    def __init__(self, inf):
        self.inf = inf

    def noHash(self):
        lines = []
        with open(self.inf, 'r', encoding='utf-8') as f_open:
            file_lines = f_open.read().split('\n')
        for line in file_lines:
            if len(line) == 0:
                continue
            lines.append(line)
        return lines

    def utf8(self):
        lines = []
        with open(self.inf, 'r', encoding='utf-8') as f_open:
            file_lines = f_open.read().split('\n')
        for line in file_lines:
            if len(line) == 0 or '#' == line[0]:
                continue
            lines.append(line)
        return lines

    def gz(self):
        lines = []
        with gzip.open(self.inf, 'rt', encoding='utf-8') as f_open:
            file_lines = f_open.read().split('\n')
        for line in file_lines:
            if len(line) == 0 or '#' == line[0]:
                continue
            lines.append(line)
        return lines


dick = {}
for i in block_cacher(openfile_V2(ing).utf8(), '>'):
    dick[i[0][1:]] = list(i[1])
n2spe = {}
spe2alt = {}
with open(inv, 'r')as f:
    for i in f.readlines():
        if i.startswith('##'):
            continue
        if i.startswith('#CHROM'):
            for n, s in enumerate(i.replace('\n', '').strip().split()[9:]):
                    n2spe[str(n)] = s
                    spe2alt[s] = []
        else:
            p = i.strip().split()
            ref = p[3]
            alt = p[4]
            chro = p[0]
            pos = p[1]
            for number, alter in enumerate(p[9:]):
                if alter == '0/0' and ref == dick[chro][int(pos)-1]:
                    spe2alt[n2spe[str(number)]].append([chro, int(pos)-1, ref])
                elif alter == '0/0' and alt == dick[chro][int(pos)-1]:
                    spe2alt[n2spe[str(number)]].append([chro, int(pos)-1, alt])
                elif (alter == '1/1' or alter == '0/1') and ref == dick[chro][int(pos)-1]:
                    spe2alt[n2spe[str(number)]].append([chro, int(pos)-1, alt])
                elif (alter == '1/1' or alter == '0/1') and alt == dick[chro][int(pos)-1]:
                    spe2alt[n2spe[str(number)]].append([chro, int(pos)-1, ref])
                elif alter == './.':
                    spe2alt[n2spe[str(number)]].append([chro, int(pos)-1, 'N'])

n = 0
for Skey in spe2alt.keys():
    with open(oD + Skey+'.SNP.fasta', 'w')as fout:
        n += 1
        print(f'Accession No.{str(n)}: {Skey} has {str(len(spe2alt[Skey]))}SNPs, Writing...')
        sfa = dick
        for line in spe2alt[Skey]:
            sfa[line[0]][line[1]] = line[2]
        for header in sfa.keys():
            fout.write('>'+header+'\n')
            fout.write(''.join(sfa[header])+'\n')
print('All Done.')
exit()
