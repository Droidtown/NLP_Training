#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from collections import Counter
from ArticutAPI import Articut
import json
import math

def wordExtractor(inputLIST, unify=True):
    '''
    配合 Articut() 的 .getNounStemLIST() 和 .getVerbStemLIST() …等功能，拋棄位置資訊，只抽出詞彙。
    '''
    resultLIST = []
    for i in inputLIST:
        if i == []:
            pass
        else:
            for e in i:
                resultLIST.append(e[-1])
    if unify == True:
        return sorted(list(set(resultLIST)))
    else:
        return sorted(resultLIST)

def counterCosineSimilarity(counter01, counter02):
    '''
    計算 counter01 和 counter02 兩者的餘弦相似度
    '''
    terms = set(counter01).union(counter02)
    dotprod = sum(counter01.get(k, 0) * counter02.get(k, 0) for k in terms)
    magA = math.sqrt(sum(counter01.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(counter02.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


def lengthSimilarity(counter01, counter02):
    '''
    計算 counter01 和 counter02 兩者在長度上的相似度
    '''

    lenc1 = sum(iter(counter01.values()))
    lenc2 = sum(iter(counter02.values()))
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))


if __name__ == "__main__":
    username = "" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
    apikey   = "" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。

    articut = Articut(username, apikey)

    baseballSTR = """本週三在紐約的比賽中，馬林魚此戰使用投手車輪戰，4名投手輪番上陣壓制大都會打線，前8局僅被敲出4支安打失1分，
    讓球隊能帶著2-1的領先優勢進入到9局下半。不過馬林魚推出巴斯登板關門，他面對首名打者麥尼爾，就被打出一發陽春砲，
    讓大都會追平比數，接下來又分別被敲出2支安打、投出保送，形成滿壘局面，此時輪到康福托上場打擊。在2好1壞的局面下，
    巴斯投了一顆內角滑球，康福托眼看這顆球越來越靠近自己的身體，似乎有下意識地將手伸進好球帶內，結果這球就直接碰觸到
    他的身肘，隨後主審庫爾帕判定這是一記觸身球，讓大都會兵不血刃拿下再見分，最終贏得比賽勝利。""".replace(" ", "").replace("\n", "")

    basketballSTR = """昨晚的紐約西區霸王之戰中，錯失勝利的太陽沒有就此束手就擒，延長賽一開始就打出7比2攻勢，米契爾和康利雖然力圖追分，
    但太陽總能馬上回應。康利讀秒階段上籃得手，布克兩罰一中，再次留給爵士追平機會。米契爾造成犯規，可惜兩罰一中，
    保羅隨後用兩罰鎖定勝利。米契爾狂轟41分8籃板3助攻，本季單場得分次高；戈貝爾16分18籃板3抄截，波格丹諾維奇20分。
    康利拿到11分4助攻，克拉克森11分，兩人合計28投僅9中。爵士的三分攻勢難以有效施展，全場44投僅11中。""".replace(" ", "").replace("\n", "")

    # 將 KNOWLEDGE_NBA_Teams.json 和 KNOWLEDGE_MLB_Teams.json 兩個體育類的字典讀取出來，合併成 mixedDICT 以後，寫入 mixedDICT.json 檔
    with open("ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_NBA_Teams.json", encoding="utf-8") as f:
        nbaDICT = json.loads(f.read())
    with open("ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_MLB_Teams.json", encoding="utf-8") as f:
        mlbDICT = json.loads(f.read())

    mixedDICT = {**nbaDICT, **mlbDICT}
    with open("mixedDICT.json", mode="w", encoding="utf-8") as f:
        json.dump(mixedDICT, f, ensure_ascii=False)

    # 將 baseballSTR 和 basketballSTR 兩篇文本各自送入 articut.parse() 裡，同時指定 userDefinedDictFILE 為剛才產生的 mixedDICT.json
    baseballResultDICT = articut.parse(baseballSTR, userDefinedDictFILE="./mixedDICT.json")
    basketballResultDICT = articut.parse(basketballSTR, userDefinedDictFILE="./mixedDICT.json")

    # 取得「動詞」做為特徵列表
    baseballVerbLIST = articut.getVerbStemLIST(baseballResultDICT)
    print("棒球文本動詞：")
    print(wordExtractor(baseballVerbLIST, unify=False))
    print("\n")
    print("籃球文本動詞：")
    basketballVerbLIST = articut.getVerbStemLIST(basketballResultDICT)
    print(wordExtractor(basketballVerbLIST, unify=False))
    print("\n")



    # 未知類別的文本
    unknownSTR01 = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))





    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("棒球文本名詞：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("籃球文本名詞：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本
    unknownSTR01 = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))




    # 取得「名詞」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("棒球文本 TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("籃球文本 TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")



    # 未知類別的文本
    unknownSTR01 = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("未知文本 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))


    # ####
    # 未知類別的文本
    unknownSTR02 = """保羅（Chris Paul）今日面對騎士再度展現他的「零失誤」功力，整場比賽打了36分鐘，拿到23分16助攻6籃板4抄截2阻攻，
    沒有出現1次失誤，這是他今年賽季第10次單場0失誤表現。根據統計，這是保羅生涯第3度至少拿到20分15助攻外加0失誤，自從1977-78年開始統計
    失誤以來，只有奈許（Steve Nash）和保羅曾3度達此高標。此外，保羅生涯共44次以0失誤表現達成助攻雙位數，在聯盟歷史上僅次於伯格斯
    （Muggsy Bogues）的46次。 """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))





    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("棒球文本名詞：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("籃球文本名詞：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本
    unknownSTR02 = """保羅（Chris Paul）今日面對騎士再度展現他的「零失誤」功力，整場比賽打了36分鐘，拿到23分16助攻6籃板4抄截2阻攻，
    沒有出現1次失誤，這是他今年賽季第10次單場0失誤表現。根據統計，這是保羅生涯第3度至少拿到20分15助攻外加0失誤，自從1977-78年開始統計
    失誤以來，只有奈許（Steve Nash）和保羅曾3度達此高標。此外，保羅生涯共44次以0失誤表現達成助攻雙位數，在聯盟歷史上僅次於伯格斯
    （Muggsy Bogues）的46次。 """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("未知文本名詞：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))




    # 取得「TF-IDF 特徵詞」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("棒球文本 TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("籃球文本 TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")



    # 未知類別的文本
    unknownSTR02 = """保羅（Chris Paul）今日面對騎士再度展現他的「零失誤」功力，整場比賽打了36分鐘，拿到23分16助攻6籃板4抄截2阻攻，
    沒有出現1次失誤，這是他今年賽季第10次單場0失誤表現。根據統計，這是保羅生涯第3度至少拿到20分15助攻外加0失誤，自從1977-78年開始統計
    失誤以來，只有奈許（Steve Nash）和保羅曾3度達此高標。此外，保羅生涯共44次以0失誤表現達成助攻雙位數，在聯盟歷史上僅次於伯格斯
    （Muggsy Bogues）的46次。 """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("未知文本 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[棒球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[籃球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))