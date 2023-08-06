import hashlib
import os
import subprocess
import sys

from prettytable import PrettyTable

codeHashList = []
fileInfo = []
title = ['文件名', '代码行数', '注释', '空行', '版本+引入', '代码行数(去注释空行)', '代码行数（去重合约+去注释空行）', '文件hash（SHA256）']
isHash = False


def dealFile(filePath, file):
    flag = False
    lineNum = 0
    comment = 0
    space = 0
    repeat = 0
    pragma = 0
    status = ''
    fileHash = sha256(filePath) + ' {}'.format(file.split('.')[0])
    with open(filePath, 'r+', encoding='utf-8')as fr:
        lines = fr.readlines()
        lineNum += len(lines)
        for line in lines:
            if line.strip().startswith('/') or line.strip().startswith('*'):
                if line.strip().startswith('/*'):
                    if line.strip().endswith('*/'):
                        pass
                    else:
                        flag = True
                elif line.strip().endswith('*/'):
                    flag = False
                comment += 1
            elif line.strip() == '':
                space += 1
            elif flag == True:
                comment += 1
            elif line.startswith('pragma') == True or line.startswith('import') == True:
                pragma += 1
            else:
                if line.startswith('contract') == True or line.startswith(
                        'interface') == True or line.startswith(
                    'library') == True or line.startswith(
                    'abstract') == True:
                    status = 'start'
                    code = ''
                    temp = 0
                    type = line.split(' ')[0]
                if status == 'start':
                    temp += 1
                    code += line
                    if line.startswith('}') == True:
                        status = 'end'
                if status == 'end':
                    status = ''
                    if isReapt(code) or type == 'abstract' or type == 'interface' or type == 'library':
                        repeat += temp
                    type = ''
    noComSpa = lineNum - comment - space - pragma
    noReapt = noComSpa - repeat
    return [file, lineNum, comment, space, pragma, noComSpa, noReapt, fileHash]


def isReapt(code):
    codeHash = hash(code)
    if codeHash in codeHashList:
        return True
    else:
        codeHashList.append(codeHash)
    return False


def printInfo():
    maxLength = 16
    table = PrettyTable()
    table.field_names = title
    table.align = 'l'
    last = [0, 0, 0, 0, 0, 0]
    for item in fileInfo:
        if len(item[0].encode()) > maxLength:
            maxLength = len(item[0].encode())
        table.add_row(item)
        for x in range(1, 7):
            last[x - 1] += item[x]
    last = ['总行数/注释/空格'] + last + ['']
    hashLine = '----------------------------------------------------------------' if isHash else '------------------'
    table.add_row(
        ['-' * maxLength, '--------', '-----', '-----', '---------', '---------------------',
         '-------------------------------',
         hashLine])
    table.add_row(last)
    print(table)


def sha256(filePath):
    if isHash == False:
        return ''
    with open(filePath, "rb") as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        return hash_value


def main():
    global isHash
    isHash = True


for root, dirs, files in os.walk("./"):
    for file in files:
        filePath = os.path.join(root, file)
        if 1:
            fileType = filePath.split('\\')[-1].split('.')[-1]
            if fileType == 'sol':
                fileInfo.append(dealFile(filePath, file))
printInfo()

if __name__ == '__main__':
    main()
