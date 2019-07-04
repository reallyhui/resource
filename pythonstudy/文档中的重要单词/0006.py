# -*- coding: utf8 -*-
import os
# os 模块提供了非常丰富的方法来处理文件和目录
import re

def findWord(Dirpath):
    #判断路径是否为目录
    if not os.path.isdir(Dirpath):
        return
    #返回指定的文件夹包含的文件或文件夹的名字的列表
    filelist=os.listdir(Dirpath)
    reObj=re.compile('\b?(\w+)\b?')
    for file in filelist:
        #把目录和文件名合成一个路径
        filePath=os.path.join(Dirpath,file)
        # print(filePath)
        #判断路径是否为文件，并且分割路径，返回路径名和文件拓展名的元组
        if os.path.isfile(filePath) and os.path.splitext(filePath)[1] == '.txt':
            with open(filePath) as f:
                data = f.read()
                words = reObj.findall(data)
                wordDict=dict()
                for word in words:
                    word = word.lower()

                    if word in ['a','the','to','and','but','or']:
                        continue
                    if word in wordDict:
                        wordDict[word]+=1
                    else:
                        wordDict[word]=1
            anslist=sorted(wordDict.items(),key=lambda t:t[1],reverse=True)
            print('file: %s->the most word: %s' % (file, anslist[1:3]))

if __name__ == '__main__':
    findWord('C:\\Users\\Administrator\\Desktop\\自兴')

