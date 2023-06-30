#!/usr/bin/env python3
import os
import argparse
import sys

def Instructions():
    Instruction = argparse.ArgumentParser(description="For job submission on Sbatch system")
    Instruction.add_argument('-s', '--scriptName', type=str,
                             help='脚本名字, 参数要求为字符串(str)', required='True')
    Instruction.add_argument('-n', '--jobName', type=str, default='run',
                             help='指定节点内存大小(单位为GB), 参数要求为整数(int)', required='True')
    Instruction.add_argument('-p', '--partition', type=str, default='low',
                             help='提交节点名, 参数要求为字符串(str)', required='True')
    Instruction.add_argument('-c', '--cpuNumber', type=int, default=1,
                             help='CPU使用数, 参数要求为整数(int)',required='True')
    Instruction.add_argument('-t', '--threadsPerCPU', type=int, default=1,
                             help='每一个CPU的线程数, 参数要求为整数(int)', required='True')
    return Instruction.parse_args()


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


if __name__ == '__main__':
    l1 = '#!/bin/bash'
    l2 = '#SBATCH --job-name='+Instructions().jobName
    l3 = '#SBATCH --partition='+Instructions().partition
    l4 = '#SBATCH --nodes='+str(Instructions().cpuNumber)
    l5 = '#SBATCH --ntasks-per-node='+str(Instructions().threadsPerCPU)
    l6 = '#SBATCH --error='+Instructions().jobName+'.err'
    l7 = '#SBATCH --output='+Instructions().jobName+'.out'
    l8 = 'CURDIR=`pwd`'
    l9 = '\n'.join(openfile(Instructions().scriptName))
    all = '\n'.join([l1, l2, l3, l4, l5, l6, l7, l8, l9])
    print('\nok，我拿到了提交脚本，是否提交?'
          '(是:敲回车; 否:Ctrl+C)\n')
    print(all)
    c = input()
    if c == '':
        with open('./' + Instructions().jobName + '.sh', 'w') as f:
            f.write('\n'.join([l1, l2, l3, l4, l5, l6, l7, l8, l9]) + '\n')
        do = os.popen('sbatch ' + Instructions().jobName + '.sh')
        print(do.read())
        do.close()
