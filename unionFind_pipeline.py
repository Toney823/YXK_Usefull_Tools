#!/usr/bin/env python3
import sys
import argparse

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if self.parent.setdefault(x, x) != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

def parse_args():
    parser = argparse.ArgumentParser(description="Union-Find grouping")
    parser.add_argument("-i", "--input", help="输入文件（tab分割）")
    parser.add_argument("-c", "--columns", nargs=2, type=int, help="指定两列（1-based）进行并查集合并")
    parser.add_argument("-p", "--pipeline", action="store_true", help="管道模式，从stdin读取")
    args = parser.parse_args()

    # 校验
    if args.pipeline and args.input:
        sys.stderr.write("Error: 管道模式下不能再指定 -i 输入文件。\n")
        sys.exit(1)
    if not args.pipeline and not args.input:
        sys.stderr.write("Error: 必须指定 -i 输入文件，或者使用 -p 从管道读取。\n")
        sys.exit(1)
    return args

def main():
    args = parse_args()
    uf = UnionFind()
    nodes = set()

    # 读取数据
    if args.pipeline:
        lines = sys.stdin.read().strip().splitlines()
    else:
        with open(args.input, 'r') as f:
            lines = f.read().strip().splitlines()

    # 默认使用前两列
    col1, col2 = (0, 1)
    if args.columns:
        col1, col2 = args.columns[0] - 1, args.columns[1] - 1

    # 构建并查集
    for line in lines:
        if not line.strip():
            continue
        parts = line.rstrip("\n").split("\t")
        if max(col1, col2) >= len(parts):
            continue
        a, b = parts[col1].strip(), parts[col2].strip()
        if a == "" and b == "":
            continue
        if a != "":
            uf.find(a)
            nodes.add(a)
        if b != "":
            uf.find(b)
            nodes.add(b)
        if a != "" and b != "":
            uf.union(a, b)

    # 分组
    groups = {}
    for node in nodes:
        root = uf.find(node)
        groups.setdefault(root, set()).add(node)

    # 排序函数：全是整数就按数值排序，否则按字符串排序
    def sort_group(lst):
        try:
            ints = sorted(int(x) for x in lst)
            return [str(x) for x in ints], (0, ints[0])
        except ValueError:
            srt = sorted(lst)
            return srt, (1, srt[0])

    grouped = []
    for g in groups.values():
        srt_list, key = sort_group(g)
        grouped.append((key, srt_list))

    # 按组内最小值排序
    grouped.sort(key=lambda x: x[0])

    for _, lst in grouped:
        print("\t".join(lst))

if __name__ == "__main__":
    main()

