import xml.etree.ElementTree as ET
import sys


if __name__ == "__main__" and len(sys.argv) != 4:
    print('This script is designed to SRA imformations from XML file downloaded from NCBI')
    print("Usage:\n\tpython3 "+ sys.argv[0] + ' <SRA_XML: STR>')
    exit()


tree = ET.parse(sys.argv[1])

root = tree.getroot()


samples_info = []


for experiment_package in root.findall('EXPERIMENT_PACKAGE'):
    experiment = experiment_package.find('EXPERIMENT')
    title = experiment.find('TITLE').text
    run_set = experiment_package.find('RUN_SET')

    for run in run_set.findall('RUN'):
        sra_id = run.get('accession')
        fastq_name = run.get('alias')

        samples_info.append({
            'SRA ID': sra_id,
            'FASTQ Name': fastq_name,
            'TITLE': title
        })

# 打印结果
for sample in samples_info:
    print(sample['SRA ID'] +'\t' + sample['FASTQ Name'] + '\t' + sample['TITLE'])
