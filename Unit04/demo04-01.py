#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from collections import Counter
from itertools import combinations

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

def counterCosineSimilarity(count1DICT, count2DICT):
    '''
    計算 count1DICT 和 count2DICT 兩者的餘弦相似度
    '''
    terms = set(count1DICT).union(count2DICT)
    dotprod = sum(count1DICT.get(k, 0) * count2DICT.get(k, 0) for k in terms)
    magA = math.sqrt(sum(count1DICT.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(count2DICT.get(k, 0)**2 for k in terms))
    similarity = dotprod / (magA * magB) if magA and magB else 0
    return similarity


def lengthSimilarity(count1DICT, count2DICT):
    '''
    計算 count1DICT 和 count2DICT 兩者在長度上的相似度
    '''

    lenc1 = sum(iter(count1DICT.values()))
    lenc2 = sum(iter(count2DICT.values()))
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))

def multiModelSimilarity(modelCountDICT, unknownCountDICT):
    '''
    多模型相似度計算
    '''
    simDICT = {}
    for key, counter in modelCountDICT.items():
        key = key[key.index("_")+1:]
        if key not in simDICT:
            simDICT[key] = 1
        simDICT[key] *= counterCosineSimilarity(unknownCountDICT, counter)
    return simDICT



if __name__ == "__main__":
    from pprint import pprint
    username = "eclair.c@droidtown.co" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
    apikey   = "ZnGXwO1emaw$z$Yrkp-Uo-VF3AO+Kvj" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。

    articut = Articut(username, apikey)

    baseballSTR = """本週三在紐約的比賽中，馬林魚此戰使用投手車輪戰，4名投手輪番上陣壓制大都會打線，前8局僅被敲出4支安打失1分，
    讓球隊能帶著2-1的領先優勢進入到9局下半。不過馬林魚推出巴斯登板關門，他面對首名打者麥尼爾，就被打出一發陽春砲，
    讓大都會追平比數，接下來又分別被敲出2支安打、投出保送，形成滿壘局面，此時輪到康福托上場打擊。在2好1壞的局面下，
    巴斯投了一顆內角滑球，康福托眼看這顆球越來越靠近自己的身體，似乎有下意識地將手伸進好球帶內，結果這球就直接碰觸到
    他的身肘，隨後主審庫爾帕判定這是一記觸身球，讓大都會兵不血刃拿下再見分，最終贏得比賽勝利。""".replace(" ", "").replace("\n", "")

    basketballSTR = """昨晚的紐約西區霸王之戰中，錯失勝利的太陽沒有就此束手就擒，延長賽一開始就打出7比2攻勢，米契爾和康利雖然力圖追分，
    但太陽總能馬上回應。康利讀秒階段上籃得手，讓布克兩罰一中，再次留給爵士追平機會。米契爾造成犯規，可惜兩罰一中，
    保羅隨後用兩罰鎖定勝利。米契爾狂轟41分8籃板3助攻，本季單場得分次高；戈貝爾16分18籃板3抄截，波格丹諾維奇20分。
    康利拿到11分4助攻，克拉克森11分，兩人合計28投僅9中。爵士的三分攻勢難以有效施展，全場44投僅11中。""".replace(" ", "").replace("\n", "")

    footballSTR = """自2006年起國際足總每屆世界盃都會公布10顆最佳進球候選名單，本屆是繼4年前之後、連2屆沒有4強以後進球入圍，
    10球有6球出現在小組賽，3球出現在16強，Neymar在本屆唯一入球也是唯一入圍的8強進球。
    Richarlison在分組首戰第73分鐘接獲Vinícius Júnior左路傳中，先用左腳將球挑高，接著躍起後空中側身用右腳將球掃入球門左下死角，
    被官方網站形容為「創造魔法」和「無法撲救」。托特納姆熱刺前鋒在16強4比1淘汰韓國時、助森巴軍團3比0領先的進球也入圍候選名單。""".replace(" ", "").replace("\n", "")


    # 將 KNOWLEDGE_NBA_Teams.json、 KNOWLEDGE_MLB_Teams.json 和 KNOWLEDGE_Football_Teams.json 兩個體育類的字典讀取出來，合併成 mixedDICT 以後，寫入 mixedDICT.json 檔
    with open("./ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_NBA_Teams.json", encoding="utf-8") as f:
        nbaDICT = json.loads(f.read())
    with open("./ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_MLB_Teams.json", encoding="utf-8") as f:
        mlbDICT = json.loads(f.read())
    with open("./ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_Football_Teams.json", encoding="utf-8") as f:
        ftbDICT = json.loads(f.read())

    mixedDICT = {**nbaDICT, **mlbDICT, **ftbDICT}
    with open("mixedDICT.json", mode="w", encoding="utf-8") as f:
        json.dump(mixedDICT, f, ensure_ascii=False)

    # 將 baseballSTR、 basketballSTR 和 football 三篇文本各自送入 articut.parse() 裡，同時指定 userDefinedDictFILE 為剛才產生的 mixedDICT.json
    baseballResultDICT = articut.parse(baseballSTR, userDefinedDictFILE="./mixedDICT.json")
    basketballResultDICT = articut.parse(basketballSTR, userDefinedDictFILE="./mixedDICT.json")
    footballResultDICT = articut.parse(footballSTR, userDefinedDictFILE="./mixedDICT.json")

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



    ## 取得「名詞」做為特徵列表
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
    print("[籃球文本 vs. 未知文本] 的 TF-IDF 特徵詞餘弦相似度:{}\n".format(basketball2unknownSIM))



    # MultiModelSimilarity
    # 取得「動詞」做為特徵列表
    verbDICT = {"baseball": articut.getVerbStemLIST(baseballResultDICT),
                "basketball": articut.getVerbStemLIST(basketballResultDICT),
                "football": articut.getVerbStemLIST(footballResultDICT),}

    # 未知類別的文本
    unknownSTR01 = """金鶯隊左投John Means今天在面對水手隊比賽中，完成一項大紀錄，那就是以27個出局數，
    在沒有保送、觸身球、失誤的狀況下完成無安打比賽，而John Means差一點就有完全比賽，主要是3局下對Sam Haggerty
    投出不死三振，差點就可以完成「完全比賽」，金鶯最終以6:0贏球。根據紀錄，金鶯隊上次左投投出無安打比賽已經是1969年，
    也是大聯盟本季第三場無安打比賽，球隊史上第10位投出無安打比賽的投手，而他也是第一位在沒有投出保送、安打、失誤，
    卻投出無安打比賽的投手。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """ 柯爾（Steve Kerr）賽後解釋道：「柯瑞出手時頭被打到了，裁判當時應該響哨。」此外，對於兩邊被吹了8次技術犯規，柯爾也認為：「這對聯盟來說，並不是一次好的展示。」
柯瑞則是表示：「每次當對手來問我，『你沒事吧』，但裁判卻不做任何表示，這種情況很有趣。我上場後其實不太在意判決的事情，但在那一個回合，我確實有點生氣。我宣洩了情緒，但感到憤怒的並不只有我。」
除了技術犯規外，勇士面對擁有制空權的公鹿，打來格外艱辛，頻頻付出犯規的代價。公鹿此役總共32次站上罰球線，比勇士多了13次。
「我一直強調，罰球不僅是送對方得分，而且當對方罰完後，你又必須得重新調整防守策略。」柯爾說。""".replace(" ", "").replace("\n", "")

    unknownSTR01 = """卡達世界盃足球賽經過廿九天、六十四戰較勁，昨天在阿根廷對戰法國的精彩冠軍戰後結束。兩隊在正規賽、延長賽的一二○分鐘分不出勝負，進入ＰＫ大戰，阿根廷最後以四比二獲勝；相隔卅六年摘下隊史第三冠，天王梅西在世界盃終於抱到大力神盃。
梅西「最後一舞」全球關注，希望阿根廷奪冠的聲量明顯壓倒法國。阿根廷上半場二比○領先，下半場被追平；延長賽也率先進球，但最後失手被追平。梅西攻進兩球，但法國隊「金童」姆巴佩上演「帽子戲法」進三球，把阿根廷逼進ＰＫ戰。
ＰＫ大戰法國隊先攻，姆巴佩打頭陣進球，阿根廷也派王牌梅西進球穩定軍心。法國第二點被阿根廷門將馬丁尼茲撲出、第三點射偏；穆阿尼負責的第四點踢進，但阿根廷前三點都踢進球門，在第四點的球越過門將防線剎那，球場上及休息區的球員、教練興奮躍起，迎接世界盃冠軍。
法國未能衛冕，讓纏繞一甲子的世界盃衛冕魔咒繼續應驗。一九六二年巴西二連霸後，接下來十四支冠軍隊全都蟬聯失利。""".replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("未知文本動詞：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")

    # 利用 Counter() 模組計算每個動詞出現的次數
    counterDICT = {"baseball": Counter(wordExtractor(verbDICT["baseball"], unify=False)),
                   "basketball": Counter(wordExtractor(verbDICT["basketball"], unify=False)),
                   "football": Counter(wordExtractor(verbDICT["football"], unify=False)),}

    #print("[Before]")
    #print(counterDICT)
    #print("[After]")
    counterDICT = counterCombination(counterDICT)
    #print(counterDICT)
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    simDICT = multiModelSimilarity(counterDICT, unknownCOUNT)

    # 計算 [已知文本 vs. 未知文本] 的餘弦相似度；
    for key, sim in simDICT.items():
        print("[未知文本 vs. {} 文本] 的動詞餘弦相似度:{}".format(key, sim))

    print("[未知文本] 與 [{} 文本] 最相似".format(max(simDICT, key = simDICT.get)))