#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
import csv
import json
import math
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
with open("account.info", encoding="utf-8") as jFILE:
    accountDICT = json.load(jFILE)
G_atk = Articut(username=accountDICT["username"], apikey=accountDICT["articut_key"])
G_modelDICT = {
    "aml": "{}/MODEL_AML.json".format(BASE_PATH),
    "other": "{}/MODEL_OTHER.json".format(BASE_PATH),
}

def getContentWord(inputSTR):
    resultDICT = {}

    result = G_atk.parse(inputSTR)
    if result["status"] == False:
        print(result["msg"])
        if result["msg"] == "Insufficient word count balance.":
            print("您的帳號剩餘可用字數不足！無法處理此次呼叫。")
        elif result["msg"] == "Your input_str is too long (over 2000 characters.)":
            print("""您的文本長度超過免費額度的「每次最多 2000 字」，請用付費帳號以避免此問題。
                  若您是為了教學而使用本程式，歡迎和我們聯絡以取得教學用支援帳號: info@droidtown.co""")
        return None
    else:
        contentWordLIST = G_atk.getContentWordLIST(result)

        for contentWord in contentWordLIST:
            for _, _, text in contentWord:
                if text not in resultDICT:
                    resultDICT[text] = 0
                resultDICT[text] += 1

        return resultDICT

def generateModel(keySTR):
    try:
        modelDICT = {model: {} for model in G_modelDICT}
        if keySTR == "aml":
            with open("../../corpus/AML_News.json", encoding="utf-8") as jFILE:
                inputSTR = "。".join(json.load(jFILE))
        elif keySTR == "other":
            with open("../../corpus/Other_News.json", encoding="utf-8") as jFILE:
                inputSTR = "。".join(json.load(jFILE))

        contentWordDICT = getContentWord(inputSTR)
        for contentWord in contentWordDICT:
            if contentWord not in modelDICT[keySTR]:
                modelDICT[keySTR][contentWord] = 0
            modelDICT[keySTR][contentWord] += contentWordDICT[contentWord]

        #for model in modelDICT:
        json.dump(modelDICT[keySTR], open(G_modelDICT[keySTR], "w", encoding="utf-8"), ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        print(str(e))
        return False

def getSimilarity(dataDICT):
    resultDICT = {}
    for model in G_modelDICT:
        modelDICT = json.load(open(G_modelDICT[model], encoding="utf-8"))
        # similarity
        unionKey = set(modelDICT).union(dataDICT)
        dotprod = sum(modelDICT.get(k, 0) * dataDICT.get(k, 0) for k in unionKey)
        magA = math.sqrt(sum(modelDICT.get(k, 0)**2 for k in unionKey))
        magB = math.sqrt(sum(dataDICT.get(k, 0)**2 for k in unionKey))
        similarity = dotprod / (magA * magB) if magA and magB else 0
        resultDICT[model] = similarity

    return resultDICT


if __name__ == "__main__":
    # 產生相關與無關 ContentWord 模型
    #status = generateModel()
    #print("GenerateModel => {}".format(status))

    # 計算 Similarity
    resultLIST = []
    with open("data.csv", newline="") as csvfile:
        rows = csv.reader(csvfile, delimiter="|")
        for row in rows:
            resultLIST.append(row)
            if row[2] == "中文摘要":
                resultLIST[-1].extend(["有關", "無關"])
                continue

            inputSTR = row[2]
            contentWordDICT = getContentWord(inputSTR)
            similarityDICT = getSimilarity(contentWordDICT)
            resultLIST[-1].extend([similarityDICT["relevant"], similarityDICT["irrelevant"]])

    if resultLIST:
        with open("result.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter="|")
            writer.writerows(resultLIST)