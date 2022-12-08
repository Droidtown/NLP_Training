#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json

from AML_run import execLoki
from Similarity import *

def news2aml(newsSTR):
    splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";"]
    nameDICT = execLoki([newsSTR], splitLIST=splitLIST)
    print(nameDICT)

    if "aml" in nameDICT.keys():
        resultLIST = []
        for i in nameDICT["aml"]:
            if i in nameDICT["innocent"]:
                pass
            elif i == "":
                pass
            else:
                resultLIST.append(i)
        return resultLIST
    else:
        print(nameDICT)
        return []



if __name__== "__main__":

    with open("../../corpus/Test_News.json", encoding="utf-8") as jFILE:
        newsLIST = json.load(jFILE)

    #文本分類

      ##產生相關與無關 ContentWord 模型
    #status = generateModel("aml")
    #print("GenerateModel => {}".format(status))
    #status = generateModel("other")
    #print("GenerateModel => {}".format(status))

      ##計算相似度
    #newsLIST = []
    #with open("../../corpus/Test_News.json", encoding="utf-8") as jFILE:
        #testLIST = json.load(jFILE)
    #for t in testLIST:
        #contentWordDICT = getContentWord(t)
        #similarityDICT = getSimilarity(contentWordDICT)
        #print(similarityDICT)
        #if similarityDICT["aml"] > similarityDICT["other"]:
            #newsLIST.append(t)

    #人名擷取結果：
    news2amlLIST = []
    for n in newsLIST:
        news2amlLIST.extend(news2aml(n.replace("、", "與")))
    news2amlLIST = sorted(list(set(news2amlLIST)))
    print("結果：{}".format(news2amlLIST))

    #正解：
    with open("../../corpus/Gold.json", encoding="utf-8") as jFILE:
        goldLIST = sorted(json.load(jFILE))

    print("正解：{}".format(goldLIST))