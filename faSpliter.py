#!/usr/bin/env python
#This script is created be yuxikai
# If anything happen yuxi.kai@163.com for u 2 contact with me
import argparse
import gzip


def Instructions():
    Instruction = argparse.ArgumentParser()
    Instruction.add_argument('-f', '--fasta', help='Your fasta file', required='True')
    Instruction.add_argument('-n', '--number', help='How many parts do you want to split', required='True')
    return Instruction.parse_args()


def block_cacher_v2(lines: list, separator_first: str):
    file_blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            continue
        if line.startswith(separator_first):
            if len(block) > 0:
                file_blocks.append(block)
            block = [line]
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


class openfile_V2:

    def __init__(self, inf):
        self.inf = inf
        return

    def utf8(inf: str):
        lines = []
        with open(inf, 'r', encoding='utf-8') as f_open:
            file_lines = f_open.read().split('\n')
        for line in file_lines:
            if len(line) == 0 or '#' == line[0]:
                continue
            lines.append(line)
        return lines

    def gz(inf: str):
        lines = []
        with gzip.open(inf, 'rt', encoding='utf-8') as f_open:
            file_lines = f_open.read().split('\n')
        for line in file_lines:
            if len(line) == 0 or '#' == line[0]:
                continue
            lines.append(line)
        return lines


def splitNumber(faL: list, n: str):
    size=int(len(faL) / int(n))
    s = []
    for i in range(0, int(len(faL)) + 1, size):
        c = faL[i:i + size]
        if c != []:
            s.append(c)
    return s


if __name__ == '__main__':
    fa = Instructions().fasta
    n = Instructions().number
    for n, i in enumerate(splitNumber([N for N in range(0, len(block_cacher_v2(openfile_V2.utf8(fa), '>')))], n)):
        with open('.'.join(fa.split('.'))+'_'+str(n+1)+'.fasta', 'w')as f:
            f.write('\n'.join(['\n'.join(block) for block in block_cacher_v2(openfile_V2.utf8(fa), '>')[i[0]:i[-1]]]))

