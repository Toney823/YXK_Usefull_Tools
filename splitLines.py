#!/usr/bin/env python3
import sys

if __name__ == "__main__" and len(sys.argv) != 3:
    print('This script is designed to split your file into multiple files')
    print("Usage:\n\tpython3 "+ sys.argv[0] + ' <InputFile: STR> <Parts: INT>\n')
    exit()


def split_list(input_list, num_splits):
    list_size = len(input_list)
    split_size = list_size // num_splits
    remainder = list_size % num_splits
    start = 0
    split_list = []
    for i in range(num_splits):
        end = start + split_size + (1 if i < remainder else 0)
        split_list.append(input_list[start:end])
        start = end
    return split_list


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


# 用法示例
input_list = openfile(sys.argv[1])
num_splits = int(sys.argv[2])
for n,i in enumerate(split_list(input_list, num_splits)):
    with open('.'.join(sys.argv[1].split('.')[:-1])+'.'+str(n+1)+'.'+sys.argv[1].split('.')[-1], 'w')as f:
        f.write('\n'.join(i)+'\n')
