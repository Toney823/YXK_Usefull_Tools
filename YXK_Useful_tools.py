import os
import os.path
import zipfile
import string
import docx
import jieba
import urllib.parse
import urllib.request
import random
import numpy as np
from scipy import stats
import re
import gzip

def category(data: list):
    # 可以找到这个list中有哪些数据（不重复的数据）
    # 例：【1，2，2，3，4，4，4，4，5，6】里面有【1，2，3，4，5，6】
    #        ^ ^     ^  ^ ^  ^ (重复部分)
    row_dict = {}
    for line in data:
        line_data = line.split('\t')
        if len(line_data) != 4:
            continue
        if line_data[0] in row_dict:
            row_dict[line_data[0]].append(line_data)
        else:
            row_dict[line_data[0]] = [line_data]
    return row_dict


def chr_extractor(in_path: str):
    # 以打开好的文件list为输入，区分出区块后对染色体序列进行判断，
    # 输出为一个【【染色体名称， 序列】xN】（N=染色体数量）的list中的list
    chr_list = []
    blocks = block_cacher(lines=openfile(path=in_path), separator_first='>')
    for block in blocks:
        if 'ptg' or 'tig' not in block[0]:
            chr_list.append('\n'.join(block))
    return chr_list


def fasta_dicker(in_fa):
    fa_db = {}
    with open(in_fa, 'r') as fin:
        for line in fin:
            if line[0] == '>':
                id = line.strip().split()[0][1:]
                fa_db[id] = []
            else:
                fa_db[id].append(line.strip())
    for id in fa_db:
        fa_db[id] = ''.join(fa_db[id])
    return fa_db


def block_cacher(lines: list, separator_first: str):
    file_blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == separator_first:
            if len(block) > 0:
                file_blocks.append(block)
            block = []
            block.append(line)
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


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


def zero_zero_number_creator(in_number: int, wanted_length: int):
    return '0' * (in_number - len(str(wanted_length))) + str(wanted_length)


def number_counting(in_list: list):
    data_dict = {}
    for key in in_list:
        data_dict[key] = data_dict.get(key, 0) + 1
    return data_dict


def merge_list(in_list01: list, in_list02: list):
    big_list = []
    for i in in_list01:
        big_list.append(i)
    for i in in_list02:
        big_list.append(i)
    return list(set(big_list))


def splitting(inlist: list):
    list1 = []
    for line in inlist:
        list1.append(line.split('\t'))
    return list1


def list_category(inlist: list):
    return list(set(inlist))


def empty_filter(in_list: list):
    lines = []
    for line in in_list:
        if len(line) == 0 or '#' in line:
            continue
        lines.append(line)
    return lines


def block_merge(block_list: list):
    # merging the block you extracted or merge your block#
    # block is a two line list, which contains a header and a sequence of this header#
    # usually when dealing with fasta_file contains protein sequence or DNA sequences#
    list1 = []
    for block in block_list:
        list1.append('\n'.join(block))
    out_str = '\n'.join(list1)
    return out_str


def write_block(merged_block_str: str, out_path: str):
    with open(out_path, 'w') as f:
        f.write(merged_block_str)


def fasta_regularization(fasta_path: str):
    merged_fasta = []
    file_blocks = block_cacher(openfile(fasta_path), '>')
    for block in file_blocks:
        merged_fasta.append([block[0], ''.join(block[1:])])
    return merged_fasta[0]


def file_blocker(path: str, separator_first: str):
    lines = []
    file_blocks = []
    block = []
    with open(path, 'r') as f:
        file_lines = f.read().split('\n')
    for line in file_lines:
        if len(line) == 0:
            continue
        lines.append(line)
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == separator_first:
            if len(block) > 0:
                file_blocks.append(block)
            block = []
            block.append(line)
            continue
        block.append(line)
    if len(block) > 0:
        file_blocks.append(block)
    return file_blocks


def block_upper(in_block: list):
    new_block = []
    for block in in_block:
        ID = block[0]
        new_seq = block[1].upper()
        new_block.append([ID, new_seq])
    return new_block


def ENC(gc3s: float):
    return 2 + gc3s + 29/((gc3s*gc3s) + (1-gc3s)*(1-gc3s))


def codonW_blk_To_preplot_txt(in_blk: str, out_toplot_txt: str):
    Phe = []
    Ser = []
    Tyr = []
    Cys = []
    Leu = []
    Ter = []
    Pro = []
    His = []
    Arg = []
    Gln = []
    Ile = []
    Thr = []
    Asn = []
    Lys = []
    Arg = []
    Met = []
    Val = []
    Ala = []
    Glu = []
    Asp = []
    Gly = []
    Trp = []
    new_block = []
    for line in openfile(in_blk):
        new_block.append(line.strip().split())
    Phe.append('Phe' + '\t' + new_block[0][1] + '\t' + new_block[0][3])
    Phe.append('Phe' + '\t' + new_block[1][0] + '\t' + new_block[1][2])
    Ser.append('Ser' + '\t' + new_block[0][5] + '\t' + new_block[0][7])
    Ser.append('Ser' + '\t' + new_block[1][3] + '\t' + new_block[1][5])
    Ser.append('Ser' + '\t' + new_block[2][4] + '\t' + new_block[2][6])
    Ser.append('Ser' + '\t' + new_block[3][3] + '\t' + new_block[3][5])
    Tyr.append('Tyr' + '\t' + new_block[0][9] + '\t' + new_block[0][11])
    Tyr.append('Tyr' + '\t' + new_block[1][6] + '\t' + new_block[1][8])
    Cys.append('Cys' + '\t' + new_block[0][13] + '\t' + new_block[0][15])
    Cys.append('Cys' + '\t' + new_block[1][9] + '\t' + new_block[1][11])
    Leu.append('Leu' + '\t' + new_block[2][1] + '\t' + new_block[2][3])
    Leu.append('Leu' + '\t' + new_block[3][0] + '\t' + new_block[3][2])
    Leu.append('Leu' + '\t' + new_block[4][0] + '\t' + new_block[4][2])
    Leu.append('Leu' + '\t' + new_block[5][0] + '\t' + new_block[5][2])
    Leu.append('Leu' + '\t' + new_block[6][0] + '\t' + new_block[6][2])
    Leu.append('Leu' + '\t' + new_block[7][0] + '\t' + new_block[7][2])
    Pro.append('Pro' + '\t' + new_block[4][4] + '\t' + new_block[4][6])
    Pro.append('Pro' + '\t' + new_block[5][3] + '\t' + new_block[5][5])
    Pro.append('Pro' + '\t' + new_block[6][3] + '\t' + new_block[6][5])
    Pro.append('Pro' + '\t' + new_block[7][3] + '\t' + new_block[7][5])
    His.append('His' + '\t' + new_block[4][8] + '\t' + new_block[4][10])
    His.append('His' + '\t' + new_block[5][6] + '\t' + new_block[5][8])
    Arg.append('Arg' + '\t' + new_block[4][12] + '\t' + new_block[4][14])
    Arg.append('Arg' + '\t' + new_block[5][9] + '\t' + new_block[5][11])
    Arg.append('Arg' + '\t' + new_block[6][10] + '\t' + new_block[6][12])
    Arg.append('Arg' + '\t' + new_block[7][9] + '\t' + new_block[7][11])
    Ile.append('Ile' + '\t' + new_block[8][1] + '\t' + new_block[8][3])
    Ile.append('Ile' + '\t' + new_block[9][0] + '\t' + new_block[9][2])
    Ile.append('Ile' + '\t' + new_block[10][0] + '\t' + new_block[10][2])
    Met.append('Met' + '\t' + new_block[11][1] + '\t' + new_block[11][3])
    Thr.append('Thr' + '\t' + new_block[8][5] + '\t' + new_block[8][7])
    Thr.append('Thr' + '\t' + new_block[9][3] + '\t' + new_block[9][5])
    Thr.append('Thr' + '\t' + new_block[10][3] + '\t' + new_block[10][5])
    Thr.append('Thr' + '\t' + new_block[11][4] + '\t' + new_block[11][6])
    Glu.append('Glu' + '\t' + new_block[6][7] + '\t' + new_block[6][9])
    Glu.append('Glu' + '\t' + new_block[7][6] + '\t' + new_block[7][8])
    Asn.append('Asn' + '\t' + new_block[8][9] + '\t' + new_block[8][11])
    Asn.append('Asn' + '\t' + new_block[9][6] + '\t' + new_block[9][8])
    Lys.append('Lys' + '\t' + new_block[10][7] + '\t' + new_block[10][9])
    Lys.append('Lys' + '\t' + new_block[11][7] + '\t' + new_block[11][9])
    Ser.append('Ser' + '\t' + new_block[8][13] + '\t' + new_block[8][15])
    Ser.append('Ser' + '\t' + new_block[9][9] + '\t' + new_block[9][11])
    Arg.append('Arg' + '\t' + new_block[10][11] + '\t' + new_block[10][13])
    Arg.append('Arg' + '\t' + new_block[11][10] + '\t' + new_block[11][12])
    Met.append('Met' + '\t' + new_block[11][1] + '\t' + new_block[11][3])
    Val.append('Val' + '\t' + new_block[12][1] + '\t' + new_block[12][3])
    Val.append('Val' + '\t' + new_block[13][0] + '\t' + new_block[13][2])
    Val.append('Val' + '\t' + new_block[14][0] + '\t' + new_block[14][2])
    Val.append('Val' + '\t' + new_block[15][0] + '\t' + new_block[15][2])
    Ala.append('Ala' + '\t' + new_block[12][5] + '\t' + new_block[12][7])
    Ala.append('Ala' + '\t' + new_block[13][3] + '\t' + new_block[13][5])
    Ala.append('Ala' + '\t' + new_block[14][3] + '\t' + new_block[14][5])
    Ala.append('Ala' + '\t' + new_block[15][3] + '\t' + new_block[15][5])
    Asp.append('Asp' + '\t' + new_block[12][9] + '\t' + new_block[12][11])
    Asp.append('Asp' + '\t' + new_block[13][6] + '\t' + new_block[13][8])
    Glu.append('Glu' + '\t' + new_block[14][7] + '\t' + new_block[14][9])
    Glu.append('Glu' + '\t' + new_block[15][6] + '\t' + new_block[15][8])
    Gly.append('Gly' + '\t' + new_block[12][13] + '\t' + new_block[12][15])
    Gly.append('Gly' + '\t' + new_block[13][9] + '\t' + new_block[13][11])
    Gly.append('Gly' + '\t' + new_block[14][10] + '\t' + new_block[14][12])
    Gly.append('Gly' + '\t' + new_block[15][9] + '\t' + new_block[15][11])
    Ter.append('*' + '\t' + new_block[2][8] + '\t' + new_block[2][10])
    Ter.append('*' + '\t' + new_block[3][6] + '\t' + new_block[3][8])
    Ter.append('*' + '\t' + new_block[2][12] + '\t' + new_block[2][14])
    Trp.append('Trp' + '\t' + new_block[3][10] + '\t' + new_block[3][12])
    Gln.append('Gln' + '\t' + new_block[6][7] + '\t' + new_block[6][9])
    Gln.append('Gln' + '\t' + new_block[7][6] + '\t' + new_block[7][8])
    new_file = []
    [new_file.append(i) for i in Ter]
    [new_file.append(i) for i in Phe]
    [new_file.append(i) for i in Ser]
    [new_file.append(i) for i in Tyr]
    [new_file.append(i) for i in Cys]
    [new_file.append(i) for i in Leu]
    [new_file.append(i) for i in Pro]
    [new_file.append(i) for i in His]
    [new_file.append(i) for i in Arg]
    [new_file.append(i) for i in Gln]
    [new_file.append(i) for i in Ile]
    [new_file.append(i) for i in Met]
    [new_file.append(i) for i in Thr]
    [new_file.append(i) for i in Asn]
    [new_file.append(i) for i in Lys]
    [new_file.append(i) for i in Val]
    [new_file.append(i) for i in Ala]
    [new_file.append(i) for i in Asp]
    [new_file.append(i) for i in Glu]
    [new_file.append(i) for i in Gly]
    [new_file.append(i) for i in Trp]
    with open(out_toplot_txt, 'w')as f:
        f.write('\n'.join(new_file))


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


class openfile_V2:

    def __init__(self, inf):
        self.inf = inf
        return

    def noHash(inf: str):
        lines = []
        with open(inf, 'r', encoding='utf-8') as f_open:
            file_lines = f_open.read().split('\n')
        for line in file_lines:
            if len(line) == 0:
                continue
            lines.append(line)
        return lines

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



def randomly_get_seq_from_fasta(in_block: list, how_many_window_do_you_want: int, how_long_seq_do_you_want: int):
    new_block = []
    for block in in_block:
        pool = []
        [pool.append(i) for i in range(0, len(block[1]) - how_long_seq_do_you_want + 1)]
        sub_block = []
        for n in range(1, how_many_window_do_you_want + 1):
            start = random.sample(pool, 1)[0]
            ending = start + how_long_seq_do_you_want + 1
            sub_block.append\
                (['>number' + str(n) + '_' + block[0][1:] + '_' + str(start) + '_' + str(ending),
                  block[1][start: ending]])
        new_block.append(sub_block)
    return new_block


def writefile_for_list(path: str, writeable_list: list, separator: str):
    with open(path, 'w') as f:
        f.write(separator.join(writeable_list))


def writefile_for_str(path: str, writeable_str: str):
    with open(path, 'w') as f:
        f.write(writeable_str)


def separator(lines: list):
    items = []
    for line in lines:
        element = line.split('\t')
        items.append(element)
    return items


def simple_listing(file_path: str):
    with open(file_path, 'r') as f:
        big_line = f.read().strip().split()
    return big_line


def assembler(separate_list: list):
    list1 = []
    for s_list in separate_list:
        list1.append('\t'.join(s_list))
    file = '\n'.join(list1)
    return file


def replace_char(old_string, char, index):
    old_string = str(old_string)
    new_string = old_string[:index] + char + old_string[index + 1:]
    return new_string


def blast_result_dealer(path: str, self_compare: str):
    lines = openfile(path)
    wanted_line = []
    wanted_line2 = []
    wanted_line3 = []
    for line in lines:
        if line[0] == '#':
            continue
        wanted_line.append(line.split('\t'))
    for line in wanted_line:
        if line[0] == line[1]:
            continue
        wanted_line2.append([line[0], line[1], line[2]])
    for line in wanted_line2:
        if self_compare in line[0] and self_compare in line[1]:
            continue
        wanted_line3.append(line)
    return wanted_line3


def how_many_individual_items_are_there_in_your_list(in_list: list):
    return len(list(set(in_list)))


def gene_extractor(gene_name_list: list, gene_sequence_blocks_list: list):
    wanted_gene_block_list = []
    for gene in gene_name_list:
        for block in gene_sequence_blocks_list:
            if gene in block[0]:
                wanted_gene_block_list.append(block)
    return wanted_gene_block_list


def allele_and_orthologous_extractor(list1: list):
    allele_list = []
    orthologous_list = []
    for line in list1:
        if 70 <= float(line[2]) < 100:
            orthologous_list.append(line)
        if float(line[2]) / 100 == 1:
            allele_list.append(line)
    return allele_list, orthologous_list


def import_os_get_unix_file(path: str):
    os.popen('cd ' + path + ' && ls > 233file.txt')
    with open(r'233file.txt', 'r') as f:
        file_list = f.read().strip().split()
    os.popen('rm 233file.txt')
    return file_list


def import_os_get_unix_commend_output(command='pwd' or 'ls'):
    os.popen(command + ' > 466666.txt')
    with open(r'466666.txt', 'r') as f:
        result = f.read().strip().split()
    os.popen('rm 466666.txt')
    return result


# New Big Boy #
def overlap_finder(three_col_list: list):
    overlap_list = []
    arranged_list = []
    for ID, start, end in three_col_list:
        if start < end:
            arranged_list.append([ID, start, end])
        else:
            arranged_list.append([ID, end, start])
    arranged_list.sort(key=lambda x: int(x[1]))
    for ii in range(1, len(arranged_list)):
        start, i2 = arranged_list[ii][1:]
        i1, l_end = arranged_list[ii - 1][1:]
        if int(start) < int(l_end):
            overlap_list.append([arranged_list[ii - 1], arranged_list[ii]])
    return overlap_list


def kmerfinder(k_mer: int, input_seq: str):
    k_list = []
    n = int(len(input_seq) - k_mer + 1)
    for i in range(0, n):
        k_list.append(input_seq[0 + i: k_mer + i])
    return k_list


def list_to_dict(lst):
    dic = {}
    for i in lst:
        if i not in dic:
            dic[i] = 1
        else:
            dic[i] += 1
    return dic


def bed_file_regulizar(in_bed: str):
    real_line = []
    wanted_bed = []
    lines = openfile(in_bed)
    for line in lines:
        if len(line) == 0:
            continue
        real_line.append(line.split('\t'))
    for line in real_line:
        if int(line[1]) < int(line[2]):
            wanted_bed.append([line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + line[3]])
        elif int(line[1]) > int(line[2]):
            wanted_bed.append([line[0] + '\t' + line[2] + '\t' + line[1] + '\t' + line[3]])
    return wanted_bed


def import_zipfile_for_zip_file(in_file: str, out_zip: str):
    zp = zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED)
    for file in in_file:
        zp.write(file)
        print('Done')


def import_jie_ba_and_docx_and_string_for_docx_processer(docx_path: str):  # 用结巴分词对文章进行分词
    file = docx.Document(docx_path)  # 处理docx文档
    wanted_combo = []
    final_combo = []
    punc = string.punctuation
    doc_T = ''
    for i in file.paragraphs:
        doc_T = doc_T + i.text
    word_combo = list(jieba.cut(doc_T, cut_all=False))
    for item in word_combo:
        if item not in punc:
            wanted_combo.append(item)
    for str_i in wanted_combo:
        if str_i.isdigit() or '：' in str_i:
            continue
        final_combo.append(str_i)
    return final_combo


def sliding_window_for_list(windowSize: int, inlist: list):
    big_window = []
    m = 0
    n = windowSize
    while n < len(inlist):
        big_window.append(inlist[m: n])
        m += windowSize
        n += windowSize
    return big_window


def sliding_window_for_string(windowSize: int, instr: str):
    big_window = []
    m = 0
    n = windowSize
    while n < len(instr):
        small_window = []
        small_window.append(instr[m: n])
        big_window.append(small_window)
        m += windowSize
        n += windowSize
    return big_window


def length_seperator(window_length: int, whole_length: int):
    windows = []
    ending = window_length
    start = 0
    while len(windows) < whole_length / window_length:
        windows.append([start, start + window_length])
        start += window_length
        ending += window_length
    return windows


def range_in__a_list__(in_n_l: list, in_range: list):
    new_list = []
    for pair_range in in_range:
        new_list.append([pair_range[0], pair_range[1], 0])
    for range_i in new_list:
        for in_n in in_n_l:
            if in_n in range(int(range_i[0]), int(range_i[1])):
                range_i[2] += 1
    return new_list


def range_in__one_number__(in_n: int, in_range: list):
    new_list = []
    for pair_range in in_range:
        new_list.append([pair_range[0], pair_range[1], 0])
    for range_i in new_list:
        if in_n in range(int(range_i[0]), int(range_i[1])):
            range_i[2] += 1
    return new_list


def import_urllib_dot_parse_url_undocing(in_list):
    final_l = []
    for i in in_list:
        final_l.append(urllib.parse.quote(i))
    return ''.join(final_l)


def import_urllib_dot_request_to_clime_bug(link: str):  # 爬虫本体, 读出https的html网络源代码
    url = link
    data = urllib.request.urlopen(url).read()
    data = data.decode('UTF-8')
    print('successfully getting the HTML data')
    return data


def import_openfile_block_cacher_fna2fasta(in_fna: str):
    new_l = []
    new_block = []
    for block in block_cacher(openfile(in_fna), '>'):
        new_block.append([block[0], ''.join(block[1:])])
    for block in new_block:
        new_line = []
        for i in block[1]:
            if i.islower():
                new_line.append(i.upper())
            elif i.isupper():
                new_line.append(i)
        new_l.append([block[0], ''.join(new_line)])
    new_f = []
    for block in new_l:
        new_f.append('\n'.join(block))
    return new_f


def import_writeFile_and_blockCachor_gff_remover(in_gff_p: str, in_list_p: str):
    dic = {}
    new_gff = []
    for line in openfile(in_gff_p):
        dic[line] = line.split('\t')[8].split('.')[0].split(';')[0].split('=')[1]
    print(len(dic.keys()))
    for key, value in list(zip(list(dic.keys()), list(dic.values()))):
        if value in openfile(in_list_p):
            continue
        else:
            new_gff.append(key)
    return new_gff


def div_file_dealer_for_RepeatMasker_and_Kimura(in_div: str, out_div: str):
    dis_lines = openfile(in_div)
    num = []
    real_num = []
    new_num = []
    new_one = []
    for line in dis_lines:
        real_num.append(line[:-2].strip().strip('[').strip("'").strip("'").split(',')[1:])
        num.append(line[:-2].strip().strip('[').strip("'").strip("'").split(',')[0])
    for i in num:
        new_num.append(i[:-1])
    for combo in list(zip(new_num, real_num)):
        new_one.append(combo[0] + '\t' + '\t'.join(combo[1]))
    with open(out_div, 'w') as f:
        f.write('\n'.join(new_one))


def import_os_to_ls(in_path: str):
    file_l = []
    for root, dir, file in list(os.walk(in_path)):
        file_l.append(file)
    return file_l[0]


def removeEmpty(in_dict_list: list):
    new_big_l = []
    for i in in_dict_list:
        if {} == i:
            continue
        new_big_l.append(i)
    return new_big_l


def comparing_want_big_one(in_n1: int, in_n2: int):
    if in_n1 > in_n2:
        return in_n1
    elif in_n2 > in_n1:
        return in_n2


def comparing_want_small_one(in_n1: int, in_n2: int):
    if in_n1 > in_n2:
        return in_n2
    elif in_n2 > in_n1:
        return in_n1


def gene_extractor_v2(in_fasta: str, in_gff3: str):
    gene_l = []

    def min_one(in_n: str):
        return str(int(in_n) - 1)

    def reversing(in_1n: str, in_2n: str, in_way: str):
        if '+' == in_way:
            return [min_one(in_1n), min_one(in_2n)]
        elif '-' == in_way:
            return [min_one(in_2n), min_one(in_1n)]

    def do_fasta(in_fa: str):
        big_dick = {}
        for block in block_cacher(openfile(in_fa), '>'):
            big_dick[block[0][1:]] = ''.join(block[1:])
        return big_dick

    dick = do_fasta(in_fasta)
    for line in openfile(in_gff3):
        if line.split('\t')[2] == 'gene':
            tmp_l = [line.split('\t')[0], line.split('\t')[-1].split(';')[0].split('=')[1]]
            for i in reversing(line.split('\t')[3], line.split('\t')[4], line.split('\t')[6]):
                tmp_l.append(i)
            gene_l.append(tmp_l)
    gene = []
    for group in gene_l:
        if int(group[2]) < int(group[3]):
            gene.append('>' + group[1] + '\n' + dick[group[0]][int(group[2]):int(group[3])])
        elif int(group[2]) > int(group[3]):
            gene.append('>' + group[1] + '\n' + dick[group[0]][int(group[3]):int(group[2])][::-1])
    return gene


def fpkm_counter(howManyReadsMappedOnYourCtg: int, TotalMappedReads: int, ctg_length: int):
    return (howManyReadsMappedOnYourCtg * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10)/(ctg_length * TotalMappedReads)


def get_p_value(arr_a: list, arr_b: list):
    a = np.array(arr_a)
    b = np.array(arr_b)
    t, p = stats.ttest_ind(a, b)
    return p


def show_path(dir_name: str):
    result = []
    for maindir, subdir, file_name_list in os.walk(dir_name):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            result.append(apath)
    return result


class filter:

    def __init__(self, input):
        self.input = input

    def filteNum(input: str):
        return re.sub(r'\d+', '', input)

    def filtestr(input: str):
        return re.sub(r'[^a-zA-Z]', '', input)


def splitNumber(faL: list, n: str):
    size=int(len(faL) / int(n))
    s = []
    for i in range(0, int(len(faL)) + 1, size):
        c = faL[i:i + size]
        if c != []:
            s.append(c)
    return s


class nStr:

    def Sum(in_str: str):
        l = []
        for i in in_str.strip().split():
            l.append(float(i))
        return sum(l)

    def Ave(in_str: str):
        l = []
        for i in in_str.strip().split():
            l.append(float(i))
        return sum(l)/len(l)

class nameLengthDicker:

    def string(in_bed: str):
        dick = {}
        for l in openfile(in_bed):
            dick[l.strip().split()[0]] = l.strip().split()[1]
        return dick

    def int(in_bed: str):
        dick = {}
        for l in openfile(in_bed):
            dick[l.strip().split()[0]] = int(l.strip().split()[1])
        return dick


def median(data):
    data.sort()
    half = len(data) // 2
    return int((data[half] + data[~half])/2)


class changeUnit:

    class base:

        def b2mb(in_n: int):
            return in_n / 1000 / 1000

        def b2gb(in_n: int):
            return in_n / 1000 / 1000 / 1000

        def b2kb(in_n: int):
            return in_n / 1000

        def kb2b(in_n: int):
            return in_n * 1000

        def gb2b(in_n: int):
            return in_n * 1000 * 1000

        def kb2gb(in_n: int):
            return in_n / 1000

        def gb2kb(in_n: int):
            return in_n * 1000

    class bit:

        def b2mb(in_n: int):
            return in_n/1024/1024

        def b2gb(in_n: int):
            return in_n/1024/1024/1024

        def b2kb(in_n: int):
            return in_n/1024

        def kb2b(in_n: int):
            return in_n*1024

        def gb2b(in_n: int):
            return in_n*1024*1024

        def kb2gb(in_n: int):
            return in_n/1024

        def gb2kb(in_n: int):
            return in_n*1024

