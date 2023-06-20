from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 以防我以后忘了这个是干啥的，这个脚本是使用selenium调用webdriver，打开虚拟浏览器，对你的氨基酸序列进行提交并保存，目的是统计氨基酸的理化性质，以下部分有提示
'''
首先需要下载一个msedgedriver,我现在的版本是114，下载链接是

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

这个脚本是专门设计在windows下进行蛋白质性状分析的脚本，如果想用的话，你可以先在第98行指定一下输入的蛋白质文件以及输出路径文件夹，然后跑一下，
有可能你下载的msedgedriver版本与与你电脑上的edge版本不一样，所以需要按照报错下载对应的msedgedriver版本，
比如我的版本是114，但是我下载的msedgedriver版本是115，那就会报错，需要重新在

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

这个网页里下载对应的版本，然后再在第68行指定这个文件的绝对路径，
注意，蛋白质是fasta格式

输出文件降是每一个蛋白质的理化性质的txt

'''


def openfile(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as f_open:
        file_lines = f_open.read().split('\n')
    for line in file_lines:
        if len(line) == 0 or '#' == line[0]:
            continue
        lines.append(line)
    return lines


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


wantedItem = {
    'Number of amino acids: ': '氨基酸数量：',
    'Molecular weight: ': '分子量：',
    'Total number of atoms: ': '氨基酸数量：',
    'Ext. coefficient': '消光系数：',
    'Aliphatic index: ': '脂肪族指数：',
    'Grand average of hydropathicity ': '蛋白质亲水性：'
}
tmpl = {}
wantedi = []

def getPEPinfo(pep: str, outDir: str):
    for b in block_cacher(openfile(pep), '>'):
        driver = webdriver.Edge(r"D:\edgedriver_win64\msedgedriver.exe")
        # 打开网页
        driver.get("https://web.expasy.org/protparam/")
        # 等待页面加载完成
        wait = WebDriverWait(driver, 10)
        form = wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        textarea = form.find_element(By.TAG_NAME, "textarea")
        textarea.send_keys(b[1])
        submit_button = form.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Compute parameters']")
        submit_button.click()
        # 等待页面加载完成
        page_text = driver.find_element(By.TAG_NAME, "body").text  # 这个page_text就是计算结果，是一个txt，你可以对他做任何txt可以做的事情

        for i in page_text.split('\n'):
            if 'Number of amino acids' in i:
                tmpl[b[0][1:]] = float(i.split(':')[1])
        for i in wantedItem.keys():
            for line in page_text.split('\n'):
                if line.startswith(i):
                    parts = line.split(':')
                    if len(parts) < 2 or len(parts[1]) == 0:
                        continue
                    wantedi.append(wantedItem[i] + ' ' + parts[1])

        # 这个部分是保存部分
        with open(outDir + b[0][1:] + '.pepInfo.shorted.txt', "w", encoding="utf-8") as f:
            f.write('\n'.join(wantedi))
        # 关闭浏览器驱动
        driver.quit()

getPEPinfo(pep=r"C:\Users\yuxik\Desktop\zq\test.pep", outDir=r"C:\Users\yuxik\Desktop\zq"+'\\')

average_molecular_weight = sum(tmpl.values()) / len(tmpl)
max_key = max(tmpl, key=tmpl.get)
min_key = min(tmpl, key=tmpl.get)

print('平均分子量:', average_molecular_weight)
print('其中最大分子量:', max_key, '，其分子量为:', tmpl[max_key])
print('分子量最小为:', min_key, '，其分子量为:', tmpl[min_key])
