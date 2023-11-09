#!/usr/bin/python3
import os.path
import urllib
import json
import requests
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import inchi
from urllib.error import HTTPError
from requests.exceptions import Timeout
import time

'''
csv 是kegg_compounds的库文件
file 是输出文件，会得到化合物分类，和kegg号
wantedNameFile 是鉴定结果，要求至少其中一列的表头是 “Name”，这一列的内容为化合物名称
round是迭代次数，默认20次，为了防止网络问题导致的掉线默认迭代20次以保证可以跑通
'''

csv = r"D:\WeChatStory\WeChat Files\wxid_6ydkydyqkwwb21\FileStorage\File\2023-11\kegg_compounds.csv"
file = r"D:\WeChatStory\WeChat Files\wxid_6ydkydyqkwwb21\FileStorage\File\2023-11\out2.txt"
wantedNameFile = r"C:\Users\yuxik\Desktop\LW\gwas\learnTTF\工作簿12.txt"
round = 20

kegg = pd.read_csv(csv)
kegg_inchikeys = []
for smi in kegg['smile'].values:
    try:
        mol = Chem.MolFromSmiles(smi)
        inchikey = inchi.MolToInchiKey(mol)
    except:
        inchikey = ''
    kegg_inchikeys.append(inchikey)
kegg['inchikey'] = kegg_inchikeys


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


def get_smiles_from_name(name: str):
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"
    operation = "name/" + name + "/property/IsomericSMILES/JSON"
    url = f"{base_url}/{operation}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Timeout:
        print("请求超时，正在重试...")
        return get_smiles_from_name(name)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    else:
        data = response.json()
        smiles = data["PropertyTable"]["Properties"][0]['IsomericSMILES']
        return smiles


def get_class_from_smiles(smiles: str):
    try:
        safe_smiles = urllib.parse.quote(smiles)
        base_url = "https://npclassifier.ucsd.edu/classify?smiles="
        url = base_url + safe_smiles
        with urllib.request.urlopen(url) as inf:
            result = inf.read()
        if result is not None:
            result = json.loads(result)['class_results'][0]
        return result
    except HTTPError as e:
        if e.code == 404:
            return None
        else:
            print("An HTTP error occurred:", e)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def get_keggid_from_smiles(smiles: str):
    try:
        mol = Chem.MolFromSmiles(smiles)
        inchikey = inchi.MolToInchiKey(mol)
    except:
        return None

    w = np.where(kegg['inchikey'].values == inchikey)
    if len(w[0]) > 0:
        keggid = kegg['ID'].values[w[0][0]]
        return keggid
    else:
        return None


out = []
df = pd.read_table(wantedNameFile)
nn = 0
n = 0

for times in range(round):
    if not os.path.exists(file):
        pass
    elif len(openfile(file)) < len(openfile(wantedNameFile))-1 and len(openfile(file)[-1].split('\t')) < 4:
        n = int(openfile(file)[-1].split('\t')[0])-1
    elif len(openfile(file)) < len(openfile(wantedNameFile))-1 and len(openfile(file)) >= 1:
        n = int(openfile(file)[-1].split('\t')[0])
    for name in df['Name'].tolist()[n:]:
        name = name.replace('"', '').replace("'", "")
        smiles = get_smiles_from_name(name)
        if smiles == 'None':
            continue
        npclass = get_class_from_smiles(smiles)
        keggid = get_keggid_from_smiles(smiles)
        n+=1
        print(f"{n}\t{name}\t{npclass}\t{keggid}")
        out.append(str(n)+'\t'+name+'\t'+str(npclass)+'\t'+str(keggid))
        time.sleep(5)
        with open(file, 'a', encoding='utf-8') as f:
            f.write(str(n)+'\t'+name+'\t'+str(npclass)+'\t'+str(keggid) + '\n')
    else:
         print('All done')
         exit()

