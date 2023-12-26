#!/usr/bin/env python3
from Bio import Phylo
import sys

if __name__ == "__main__" and len(sys.argv) != 3:
    print('This script is designed to change the nodes ID by a index file')
    print("Usage:\n\tpython3 "+ sys.argv[0] + ' <inNWK: STR>  <outNWK: STR> <indexFile: STR>\n')
    print('Requirements:\n\tBiopython: pip install biopython')
    exit()


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


def save_tree_with_new_names(tree_in, tree_out, name_subs):
    print()
    print('Writing Microreact tree to: {}'.format(tree_out))
    tree_format = None
    for try_tree_format in ['newick', 'nexus', 'nexml', 'phyloxml', 'cdao']:
        try:
            Phylo.read(tree_in, try_tree_format)
            tree_format = try_tree_format
            break
        except ValueError:
            pass
    if tree_format is None:
        sys.exit('Error: could not read input tree')

    tree = Phylo.read(tree_in, tree_format)
    for node in tree.get_terminals():
        name = str(node.name)
        try:
            node.name = name_subs[name]
        except IndexError:
            sys.exit('Error: sample name in tree not in Kleborate data: ' + name)
    Phylo.write(tree, tree_out, 'newick')


t = sys.argv[1]#r"C:\Users\yuxik\Desktop\LW\gwas\homoSeperation\outmat_mat_fastme\outmat_mat_fastme-tree.nwk"
to = sys.argv[2]#r"C:\Users\yuxik\Desktop\LW\gwas\homoSeperation\outmat_mat_fastme\outmat_mat_fastme-tree.out.nwk"
index = sys.argv[3]#r"C:\Users\yuxik\Desktop\LW\gwas\homoSeperation\index.txt"
name = {i.split('\t')[1]: i.split('\t')[0] for i in openfile(index)}
save_tree_with_new_names(t, to, name)

