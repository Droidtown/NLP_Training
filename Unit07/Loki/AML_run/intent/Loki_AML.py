#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for AML

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

import json
import os

DEBUG_AML = True
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except:
    userDefinedDICT = {}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_AML:
        print("[AML] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[B][公司][董事長][蔡宏安]及[總經理][王建樹]因[資金][需求]":
        resultDICT["aml"].append(args[3])
        resultDICT["aml"].append(args[5])

    if utterance == "[C][公司][負責人][葉曦瑩]為逃漏營利[事業][所得稅]":
        resultDICT["aml"].append(args[3])

    if utterance == "[H][公司][負責人][張育民]於模里西斯與[美國]與[香港]及[汶萊]等[地]設立[G]等境[外公][司]":
                resultDICT["aml"].append(args[3])

    if utterance == "[R][集團][負責人][尹德昌]與[汪曉明]指示[員工]勾結[E]等合作[廠商][員工]偽造[不實]買賣[合約書]與統一[發票]與[出貨單]及[海][運提單]等[文件]":
        resultDICT["aml"].append(args[3])
        resultDICT["aml"].append(args[4])

    if utterance == "[T][公司][董事][杜立賓]及[S][公司][董事][高進安][實際]參與洽談[過程]":
        resultDICT["aml"].append(args[3])
        resultDICT["aml"].append(args[7])

    if utterance == "[事後]向[蔡明德]收取約定之[回][扣]共計[新臺幣][3,950萬元]":
        resultDICT["aml"].append(args[1])

    if utterance == "[何奕安]並自備[熱敏票]據打[印機]":
        resultDICT["aml"].append(args[0])

    if utterance == "[何奕安]以微信通訊[軟體]支付[人民幣][貨款]之[方式]":
        resultDICT["aml"].append(args[0])

    if utterance == "[何奕安]再以[事先]購買之[外勞][卡門號]登入[蝦皮人頭][帳號]":
        resultDICT["aml"].append(args[0])

    if utterance == "[另]由不知情之[物流][公司]在[臺]報關[接貨]及送貨至[毛頌恩]承租之[倉庫]":
        resultDICT["aml"].append(args[5])

    if utterance == "[吳定國][先後]於[彰化縣]及[臺中市]多[個][處所]":
        resultDICT["aml"].append(args[0])

    if utterance == "[吳定國][委]由不知情之[第三方]支付[公司]為代收收款[方]":
        resultDICT["aml"].append(args[0])

    if utterance == "[嚴政蘭]指示親屬或以每人[新臺幣][15萬元]至[60萬元]尋找[人頭][公司][負責人]":
        resultDICT["aml"].append(args[0])

    if utterance == "[姚仁傑]以其擔任[負責人]之[W][公司名義]":
        resultDICT["aml"].append(args[0])

    if utterance == "[姚仁傑]與[潘志安][二]人為牟取不法[利益]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[尹德昌]與[汪曉明]即[自行]或指示[員工]提領[R][集團帳戶][款項]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[尹德昌]與[汪曉明]等人無預警失聯":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[廖佑安]係[S][公司]負責人":
        resultDICT["aml"].append(args[0])

    if utterance == "[廖志傑]任職於[該][公司]":
        resultDICT["aml"].append(args[0])

    if utterance == "[廖灝汶]與[廖灝俐]各於[臉書]經營[社團]販賣[越南][香菸]及[肉製品]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[廖灝汶]與[廖灝俐]負責在[臺][接貨]及轉運[貨品]予在[臺購][貨客戶]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[張育民][擅自][陸續][將][G]等[人頭][公司帳戶][內]總計[3億餘元][款項]匯往[L]掌控之[境][外][法人][帳戶]侵占入己":
        resultDICT["aml"].append(args[0])

    if utterance == "[張育民]並以[H][公司][員工]或[友人]擔任[人頭][負責人]":
        resultDICT["aml"].append(args[0])

    if utterance == "[彭國盛]因恐炒股[資金][不足]":
        resultDICT["aml"].append(args[0])

    if utterance == "[後][張育民]於未經[董事][會]同意[下]":
        resultDICT["aml"].append(args[1])

    if utterance == "[曾國琳]與[林力達]與[何友山]及[王呈蓮]於[103年][間][共同]發起與主持操縱":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])
        resultDICT["aml"].append(args[2])
        resultDICT["aml"].append(args[3])

    if utterance == "[李進杰]係[某][政府][機關][秘書長]":
        resultDICT["aml"].append(args[0])

    if utterance == "[林嘉良][配偶][潘慧萍]及[胞妹][潘慧怡]於[林嘉良]閒聊[中]得悉[此事]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[2])
        resultDICT["aml"].append(args[4])

    if utterance == "[林嘉良]受[T][公司]委託製作[股權][合理][性][意見書]":
        resultDICT["aml"].append(args[0])

    if utterance == "[林建國][先生][長期]無[業]無法[合理]交待[金錢][來源]":
        resultDICT["aml"].append(args[0])

    if utterance == "[林建國][先生]與[男子][高宏貴]合作":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[3])

    if utterance == "[歐建豪]與[江宗發]等[人杜]撰渠等成立之[臺偽政府]已獲[美國][軍事政府]承認":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[歐建豪]與[江宗發]等人又以辦理[臺偽政府]代訓[政務][人員][相關][職務]訓練[課程]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[毛頌恩]並雇用[員工]協助包裝進口轉運[貨品]供[物流業][者]送交[購][貨客戶]":
        resultDICT["aml"].append(args[0])

    if utterance == "[毛頌恩]與[廖志傑]與[廖灝汶]等人於[110年8月][間][透][過於]空運[併袋貨][中][私]運夾藏[方式]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])
        resultDICT["aml"].append(args[2])

    if utterance == "[汪利行]即[命][曹世達]等人以[面]交[方式]支付[前揭]約定[數額]之[新臺幣][現金]予[客戶]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[2])

    if utterance == "[汪利行]即指派[曹世達]等人向[客戶]收取[新臺幣][現金]並取得[客戶]指定匯入之[大陸][地區][帳戶]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[汪利行]指示[沈宗德]與[林照山]以每戶[新臺幣][1萬5,000元][起][價格]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])
        resultDICT["aml"].append(args[2])

    if utterance == "[簡尚德]與[潘慧萍]及[潘慧怡]等人於[重大][訊息]公告[前]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])
        resultDICT["aml"].append(args[2])

    if utterance == "[簡裕民]並提供本人及[友人][證券帳戶]配合[彭國盛]指示[價量]下單[交易]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[3])

    if utterance == "[蔡宏安]為維持[B][公司股價]避免遭[銀行]提徵[擔保品]與追繳或[股票]遭斷頭":
        resultDICT["aml"].append(args[0])

    if utterance == "[記者][鄧木卿][台中]報導":
        resultDICT["aml"].append(args[1])

    if utterance == "[誆]騙支持[者]交付[現金]予[毛明政]等工作[人員]":
        resultDICT["aml"].append(args[3])

    if utterance == "[馬怡貞]與[白品良]以[境][外][D][集團][臺灣][區][負責人][名義]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[馬怡貞]與[白品良]等人[非法]吸金[金額]累計達[新臺幣][65億4,472萬餘元]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "[高進安][事後][將]收購[訊息]透露[友人][簡尚德]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[5])

    if utterance == "[黎仁湘]於[109年][間]加入[年][籍]不[詳][B]成立之犯罪[集團]":
        resultDICT["aml"].append(args[0])

    if utterance == "並依[葉俊琪]指示承租[高雄市][某][址]設立[S]洗錢[機房]":
        resultDICT["aml"].append(args[0])

    if utterance == "並由[毛頌恩]負責在[越南]進貨與報關[事宜]":
        resultDICT["aml"].append(args[0])

    if utterance == "以[WhatsApp]向[汪利行]等人詢價":
        resultDICT["aml"].append(args[1])

    if utterance == "以[每月][新臺幣][3萬5,000元]聘僱[顧雲淳]等[8]人":
        resultDICT["aml"].append(args[3])

    if utterance == "使用[葉俊琪]提供之[大陸][地區][人頭][金融][帳戶]與[U][盾]":
        resultDICT["aml"].append(args[0])

    if utterance == "使用[蔡宏安]本人及多[個]向[員工]":
        resultDICT["aml"].append(args[0])

    if utterance == "供[何奕安]黏貼於廉價化[粧品]及保養[品][上]":
        resultDICT["aml"].append(args[0])

    if utterance == "再以[國際][航空郵件]包[裏][方式][將][該][大麻郵]包郵寄至[林建國][臺北市][住處]":
        resultDICT["aml"].append(args[7])

    if utterance == "又於[林建國][住處]查扣[毒品][大麻][139公克]與販賣[大麻資料]及[新臺幣][24萬7,000元][現金]":
        resultDICT["aml"].append(args[0])

    if utterance == "另於[林建國]租用之[銀行][保險][箱][內]扣得[新臺幣][960萬元][現金]":
        resultDICT["aml"].append(args[0])

    if utterance == "向有意投標之[N][公司][實際][負責人][蔡明德]索取[回扣]":
        resultDICT["aml"].append(args[4])

    if utterance == "在[P]確認收到[客戶]匯入[汪利行]等人收購之[大陸][地區][金融][帳戶][款項][後]":
        resultDICT["aml"].append(args[2])

    if utterance == "復向[Y][證券][公司][營業員]兼[市場金主][簡裕民]商借[資金]":
        resultDICT["aml"].append(args[5])

    if utterance == "復由[汪利行]透過[何燦得]指示[潘念慈]以[網路]轉帳[方式]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "或匯款至[歐建豪]與[江宗發][實際]控制之[臺偽政府][基金會][境][外][金融][機構帳戶]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "或匯款至[歐書豪]等工作[人員][名下][金融][帳戶]":
        resultDICT["aml"].append(args[0])

    if utterance == "支付[款項]予[歐建豪]與[江宗發]等人申辦[臺偽政府]發行[證件]":
        resultDICT["aml"].append(args[1])
        resultDICT["aml"].append(args[2])

    if utterance == "改由起訴[前][消防署長][黃季敏]涉貪的[殺手][級][檢察官][黃珮瑜]接手偵辦":
        resultDICT["aml"].append(args[2])

    if utterance == "由[尹德昌]與[汪曉明]持[不實][交易文件][陸續]向[國內][銀行]申辦[應]收[帳款]融資及外銷放款":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "由[林建國]出資委託[高宏貴]於[境][外]自[網路][黑市]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "由[汪利行]參考[當日][金融][機構][人民幣][牌]告[匯率]加計[2%][利潤][後]":
        resultDICT["aml"].append(args[0])

    if utterance == "經執法[機關]查獲[該][127公克][大麻郵]包並[循線]逮捕[林建國]":
        resultDICT["aml"].append(args[5])

    if utterance == "總計[蔡宏安]與[彭國盛]等人[共]使用[32]人[87個][證券][帳戶]":
        resultDICT["aml"].append(args[0])
        resultDICT["aml"].append(args[1])

    if utterance == "與[股市]作手[彭國盛]以[彭國盛]本人及[彭國盛][親友][譚永立]等人[證券帳戶]":
        resultDICT["aml"].append(args[1])
        resultDICT["aml"].append(args[2])
        resultDICT["aml"].append(args[3])
        resultDICT["aml"].append(args[5])

    return resultDICT