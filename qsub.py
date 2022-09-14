#!/usr/bin/env python
import os
import argparse
import random


def Instructions():
    Instruction = argparse.ArgumentParser()
    Instruction.add_argument('-c', '--cpuNumber', help='福建省超算上‘rtm单核单线程’，你的线程数和核数要相等, 参数要求为整数(int)', required='True')
    Instruction.add_argument('-m', '--mem', help='指定节点内存大小(单位为GB), 参数要求为整数(int)', required='True')
    Instruction.add_argument('-s', '--script', help='你的脚本.sh文件, 参数要求为字符串类型(绝对路径，使用命令pwd可得到)', required='True')
    return Instruction.parse_args()


def getSHARE():
    pool = os.popen('qstat -Qf share')
    o = pool.read()
    pool.close()
    freePBN = []
    for i in o.split('\n'):
        if ':' in i or '=' in i:
            continue
        for ii in i.split(','):
            iii = ii.strip().split()
            if len(iii) == 1:
                freePBN.append(iii[0])
            if len(iii) == 0:
                continue
    return freePBN


real_pool = getSHARE()


def getAVAPBS():
    pool2 = os.popen('pestat')
    o2 = pool2.read()
    pool2.close()
    avPBS = []
    for col in o2.split('\n'):
        sPool = col.strip().split()
        if len(sPool) == 0:
            continue
        elif len(sPool[-1]) <= 6 and sPool[0] in real_pool and sPool[1] == 'free':
            avPBS.append(sPool[0])
    return avPBS


if __name__ == '__main__':
    print('由于近期反复提交任务出现内存报错，需要手动挑选内存，为了节省时间我写了这个脚本\n'
          'enjoy...')
    avPBS = getAVAPBS()
    cmd = 'qsub -d ./ -l mem='+str(Instructions().mem)+'GB,nodes='+random.choice(avPBS)+':ppn='+str(Instructions().cpuNumber)+' -q share -o '+'.'.join(Instructions().script.split('.')[:-1]) + '.log -e '+'.'.join(Instructions().script.split('.')[:-1])+'.err '+Instructions().script
    print(cmd)
    print('ok，我拿到了提交命令，是否提交'
          '(是:敲回车; 否:Ctrl+C)')
    c = input('你确定?')
    if c == '':
        do = os.popen(cmd)
        print(do.read())
        do.close()
