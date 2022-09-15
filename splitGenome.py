#!/usr/bin/env python
import os
import sys

def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


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


d = './'+'.'.join(sys.argv[1].split('.')[:-1])
os.makedirs(d)
for block in block_cacher_v2(openfile(sys.argv[1]), '>'):
    b = '\n'.join(block)
    with open(d+'/'+'_'.join(block[0][1:].strip().split())+'.fasta', 'w')as f:
        f.write(b)
