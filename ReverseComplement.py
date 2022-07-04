#!/usr/bin/env python
import os
import argparse


def Instructions():
    Instruction = argparse.ArgumentParser()
    Instruction.add_argument('-f', '--fasta', help='Your sequence file', required='True')
    Instruction.add_argument('-s', '--start', help='The startinng point of your region', required='True')
    Instruction.add_argument('-e', '--end', help='The ending point of your region', required='True')
    return Instruction.parse_args()


db = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}


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


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


def regularFa(in_fa: str):
    new_f = []
    for block in block_cacher_v2(openfile(in_fa), '>'):
        new_f.append(block[0])
        new_f.append(''.join(block[1:]))
    return new_f


def reverse(in_fasta: str, start: str, end: str):
    new_block = []
    blocks = regularFa(in_fasta)
    tmp_l = []
    tmp_ll = []
    new_block.append(blocks[0])
    tmp_ll.append(blocks[1][:int(start)])
    for i in blocks[1][int(start):int(end)]:
        tmp_l.append(db[i])
    tmp_ll.append(''.join(tmp_l[::-1]))
    tmp_ll.append(blocks[1][int(end):])
    new_block.append(''.join(tmp_ll))
    return new_block


def writeFa(in_f: str, s: str, e: str):
    with open('.'.join(in_f.split('.')[:-1]) + '.reversing_' + s + '_' + e + '.fasta', 'w')as f:
        f.write('\n'.join(reverse(in_fasta=in_f, start=s, end=e))+'\n')


if __name__ == '__main__':
    print('The scripts only designed for \
    reverse complement of only one sequence at a time, \
    please make sure your input region is single! :b\n\
                 Usage: python ' + os.getcwd() + '/ReverseComplement.py -f [dir/str] -s [startPoint/int] -e [endPoint/int]')
    ins = Instructions()
    in_f = ins.fasta
    s = ins.start
    e = ins.end
    writeFa(in_f=in_f, s=s, e=e)
