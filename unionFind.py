#!/usr/bin/env python3
import argparse

class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        else:
            self.parent[rb] = ra
            if self.rank[ra] == self.rank[rb]:
                self.rank[ra] += 1


def main():
    p = argparse.ArgumentParser(description="仅用两列做并查集合并并打印（tab 分割，列号 1-based）")
    p.add_argument("-i", "--input", required=True, help="输入文件（tab 分割）")
    p.add_argument("-c", "--columns", nargs=2, type=int, default=[1,2],
                   help="指定两个列号（1-based），例如 -c 1 2。默认 1 2。")
    args = p.parse_args()

    col1, col2 = args.columns
    if col1 <= 0 or col2 <= 0:
        raise SystemExit("列号必须为正整数（1-based）。")
    col1 -= 1
    col2 -= 1

    uf = UnionFind()
    nodes = set()

    with open(args.input, 'r') as fh:
        for line in fh:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            a = parts[col1].strip() if 0 <= col1 < len(parts) else ""
            b = parts[col2].strip() if 0 <= col2 < len(parts) else ""
            if a == "" and b == "":
                continue
            if a != "":
                uf.find(a); nodes.add(a)
            if b != "":
                uf.find(b); nodes.add(b)
            if a != "" and b != "":
                uf.union(a, b)

    # 分组
    groups = {}
    for node in nodes:
        root = uf.find(node)
        groups.setdefault(root, []).append(node)

    # 排序规则：如果组内全是整数就按数值排，否则按字符串排
    def sort_group(lst):
        try:
            ints = [int(x) for x in lst]
            ints.sort()
            return [str(x) for x in ints], (0, ints[0])
        except ValueError:
            srt = sorted(lst)
            return srt, (1, srt[0])

    grouped = []
    for g in groups.values():
        srt_list, key = sort_group(g)
        grouped.append((key, srt_list))

    # 按组内最小值排序，整数组优先
    grouped.sort(key=lambda x: x[0])

    for _, lst in grouped:
        print("\t".join(lst))


if __name__ == "__main__":
    main()

