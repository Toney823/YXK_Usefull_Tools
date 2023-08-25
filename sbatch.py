#!/usr/bin/env python3
#Created by yuxikai
import os
import argparse
import sys


def Instructions():
    Instruction = argparse.ArgumentParser(description="For job submission on Sbatch system \nUsage 101:\nfor i in {1..10}; do echo 'echo '${i} >> do.sh\nsbatch.py -s do.sh -n test -p low -c 1 -t 1")
    Instruction.add_argument('-s', '--scriptName', type=str,
                             help='脚本名字, 参数要求为字符串(str)', required=True)
    Instruction.add_argument('-n', '--jobName', type=str, default='run',
                             help='指定任务名, 参数要求为字符串(str)', required=True)
    Instruction.add_argument('-p', '--partition', type=str, default='low',
                             help='提交节点名, 参数要求为字符串(str), 如low big; 或者连续添加备用节点如: low,big,smp01', required=True)
    Instruction.add_argument('-c', '--cpuNumber', type=int, default=1,
                             help='CPU使用数, 参数要求为整数(int)',required=True)
    Instruction.add_argument('-t', '--threadsPerCPU', type=int, default=1,
                             help='每一个CPU的线程数, 参数要求为整数(int)', required=True)
    Instruction.add_argument('-srun', '--cmdLineRunning', type=str,
                        help='是否使用srun运行任务, '
                             '不添加即为默认不使用srun, 若添加此参数，将生成一个记录使用过该命令的历史文件, '
                             '将以任务名对该文件进行命名,\n注意!!! 此参数只适合运行单行命令!!!')
    Instruction.add_argument('-y', '--yes',
                             help='是否直接提交, '
                                  '')
    return Instruction.parse_args()


def openfile(path: str, nohash: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    if nohash == 'False':
        for line in file_lines:
            if len(line) == 0:
                continue
            lines.append(line)
        return lines
    elif nohash == 'True':
        for line in file_lines:
            if len(line) == 0 or '#' == line[0]:
                continue
            lines.append(line)
        return lines


if __name__ == '__main__':
    # if os.path.exists('~/.sbatchPy/') == False:
    #     os.system('mkdir ~/.sbatchPy/')
    #     cmdStore = {}
    #     cmdl = []
    #     for n, cmd in enumerate(openfile(Instructions().scriptName, nohash='True')):
    #         cmdStore[n] = cmd
    #         cmdl.append(str(n+1)+'.\t'+cmd)
    #     with open('~/.sbatchPy/'+Instructions().jobName+'.History.txt', 'r')as f:
    #         f.write('#Attention! This file stores the command about ' + Instructions().jobName+'\n' + '\n'.join(cmdl)+'\n')
    #     if os.path.exists('~/.sbatchPy/'+Instructions().jobName+'.History.txt') == True:
    #         finalN = int(openfile('~/.sbatchPy/'+Instructions().jobName+'.History.txt', nohash='True')[-1].split('\t')[0].replace('.', ''))
    #         cmdStore = {}
    #         cmdl = []
    #         for cmd in openfile(Instructions().scriptName, nohash='True'):
    #             finalN += 1
    #             with open('~/.sbatchPy/'+Instructions().jobName+'.History.txt', 'a')as f:
    #                 f.write(str(finalN+1)+'.\t'+cmd+'\n')
    #     if os.path.exists('~/.sbatchPy/'+Instructions().jobName+'.History.txt') == False:
    #         with open('~/.sbatchPy/' + Instructions().jobName + '.History.txt', 'r') as f:
    #             f.write('#Attention! This file stores the command about ' + Instructions().jobName + '\n' + '\n'.join(
    #                 cmdl) + '\n')
    if Instructions().cmdLineRunning == 'no':
        l1 = '#!/bin/bash'
        l2 = '#SBATCH --job-name='+Instructions().jobName
        l3 = '#SBATCH --partition='+Instructions().partition
        l4 = '#SBATCH --nodes='+str(Instructions().cpuNumber)
        l5 = '#SBATCH --ntasks-per-node='+str(Instructions().threadsPerCPU)
        l6 = '#SBATCH --error='+Instructions().jobName+'.err'
        l7 = '#SBATCH --output='+Instructions().jobName+'.out'
        l8 = 'CURDIR=`pwd`'
        l9 = 'cd ' + os.path.abspath('./')+'/'
        l10 = '\n'.join(openfile(Instructions().scriptName, nohash='True'))
        all = '\n'.join([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])
        print(all)
        print('\nok, 我拿到了提交脚本, 是否提交?'
              '(是:敲Enter; 否:Ctrl+C)\n')
        c = input()
        if c == '':
            try:
                with open('./' + Instructions().jobName + '.sh', 'w') as f:
                    f.write('\n'.join([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]) + '\n')
                do = os.popen('sbatch ' + Instructions().jobName + '.sh')
                print(do.read())
                do.close()
            except Exception as e:
                print('提交作业出错: \n', str(e))
    if Instructions().cmdLineRunning == 'yes':
        cmd = openfile(Instructions().scriptName, nohash='True')[0]
        historyFile = Instructions().jobName+'.history.txt'
        with open(historyFile, 'a')as f:
            f.write(cmd+'\n')
        run = 'srun -p ' + Instructions().partition + ' --nodes ' + str(Instructions().cpuNumber) + ' -c ' + str(Instructions().threadsPerCPU) + ' ' + cmd
        print('command is: ')
        print('\t' + run)
        print('\nok, The following line is your command, submit?'
              '(Yep: Hit Enter; Nope: Ctrl+C)\n')
        c = input()
        if c == '':
            try:
                do = os.popen(run)
                print(do.read())
                do.close()
            except Exception as e:
                print('srun went wrong, please Check:\n', str(e))
    elif Instructions().yes == 'yes':
        cmd = openfile(Instructions().scriptName, nohash='True')[0]
        historyFile = Instructions().jobName + '.history.txt'
        with open(historyFile, 'a') as f:
            f.write(cmd + '\n')
        l1 = '#!/bin/bash'
        l2 = '#SBATCH --job-name=' + Instructions().jobName
        l3 = '#SBATCH --partition=' + Instructions().partition
        l4 = '#SBATCH --nodes=' + str(Instructions().cpuNumber)
        l5 = '#SBATCH --ntasks-per-node=' + str(Instructions().threadsPerCPU)
        l6 = '#SBATCH --error=' + Instructions().jobName + '.err'
        l7 = '#SBATCH --output=' + Instructions().jobName + '.out'
        l8 = 'CURDIR=`pwd`'
        l9 = 'cd ' + os.path.abspath('./') + '/'
        l10 = '\n'.join(openfile(Instructions().scriptName, nohash='True'))
        all = '\n'.join([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])
        print('Sbatch Submission is \n' + all)
        with open('./' + Instructions().jobName + '.sh', 'w') as f:
            f.write('\n'.join([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]) + '\n')
        do = os.popen('sbatch ' + Instructions().jobName + '.sh')
        print('Submission is done!')

