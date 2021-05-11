#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from ArticutAPI import Articut
import json

def wordExtractor(inputLIST):
    '''
    配合 Articut() 的 .getNounStemLIST() 和 .getVerbStemLIST() 拋棄位置資訊，只抽出詞彙。
    '''
    resultLIST = []
    for i in inputLIST:
        if i == []:
            pass
        else:
            for e in i:
                resultLIST.append(e[-1])
    return sorted(list(set(resultLIST)))


if __name__ == "__main__":
    username = "" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
    apikey   = "" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。

    articut = Articut(username, apikey)

    baseballSTR = """馬林魚此戰使用投手車輪戰，4名投手輪番上陣壓制大都會打線，前8局僅被敲出4支安打失1分，
    讓球隊能帶著2-1的領先優勢進入到9局下半。不過馬林魚推出巴斯登板關門，他面對首名打者麥尼爾，就被打出一發陽春砲，
    讓大都會追平比數，接下來又分別被敲出2支安打、投出保送，形成滿壘局面，此時輪到康福托上場打擊。在2好1壞的局面下，
    巴斯投了一顆內角滑球，康福托眼看這顆球越來越靠近自己的身體，似乎有下意識地將手伸進好球帶內，結果這球就直接碰觸到
    他的身肘，隨後主審庫爾帕判定這是一記觸身球，讓大都會兵不血刃拿下再見分，最終贏得比賽勝利。""".replace(" ", "").replace("\n", "")

    basketballSTR = """錯失勝利的太陽沒有就此束手就擒，延長賽一開始就打出7比2攻勢，米契爾和康利雖然力圖追分，
    但太陽總能馬上回應。康利讀秒階段上籃得手，布克兩罰一中，再次留給爵士追平機會。米契爾造成犯規，可惜兩罰一中，
    保羅隨後用兩罰鎖定勝利。米契爾狂轟41分8籃板3助攻，本季單場得分次高；戈貝爾16分18籃板3抄截，波格丹諾維奇20分。
    康利拿到11分4助攻，克拉克森11分，兩人合計28投僅9中。爵士的三分攻勢難以有效施展，全場44投僅11中。""".replace(" ", "").replace("\n", "")

    # Week01:
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


    # Week02
    # 取得 TF-IDF 特徵詞列表
    baseball_TFIDF = articut.analyse.extract_tags(baseballResultDICT)
    #print(baseball_TFIDF)

    basketball_TFIDF = articut.analyse.extract_tags(basketballResultDICT)
    #print(basketball_TFIDF)

    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    #print(wordExtractor(baseballNounLIST))

    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    #print(wordExtractor(basketballNounLIST))

    # 取得「動詞」做為特徵列表
    baseballVerbLIST = articut.getVerbStemLIST(baseballResultDICT)
    print(wordExtractor(baseballVerbLIST))

    basketballVerbLIST = articut.getVerbStemLIST(basketballResultDICT)
    print(wordExtractor(basketballVerbLIST))

