#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 3.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No matching Intent."
                }
            ]
        }
"""

from requests import post
from requests import codes
import math
import re
try:
    from intent import Loki_AML
    from intent import Loki_Innocent
except:
    from .intent import Loki_AML
    from .intent import Loki_Innocent


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = "peter.w@droidtown.co"
LOKI_KEY = "XJAOH7R3iLOrMQ$uCeuG6fMvL_%6&4k"
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []
INPUT_LIMIT = 20

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "{} Connection failed.".format(result.status_code)
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    # 將 intent 會使用到的 key 預先設爲空列表
    resultDICT = {
       "aml":[],
       "innocent":[]
    }
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # AML
                if lokiRst.getIntent(index, resultIndex) == "AML":
                    resultDICT = Loki_AML.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Innocent
                if lokiRst.getIntent(index, resultIndex) == "Innocent":
                    resultDICT = Loki_Innocent.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def execLoki(content, filterLIST=[], splitLIST=[]):
    """
    input
        content       STR / STR[]    要執行 loki 分析的內容 (可以是字串或字串列表)
        filterLIST    STR[]          指定要比對的意圖 (空列表代表不指定)
        splitLIST     STR[]          指定要斷句的符號 (空列表代表不指定)
                                     * 如果一句 content 內包含同一意圖的多個 utterance，請使用 splitLIST 切割 content

    output
        resultDICT    DICT           合併 runLoki() 的結果，請先設定 runLoki() 的 resultDICT 初始值

    e.g.
        splitLIST = ["！", "，", "。", "？", "!", ",", "
", "；", "　", ";"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？")                      # output => ["今天天氣"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？", splitLIST=splitLIST) # output => ["今天天氣", "後天氣象"]
        resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"])                # output => ["今天天氣", "後天氣象"]
    """
    contentLIST = []
    if type(content) == str:
        contentLIST = [content]
    if type(content) == list:
        contentLIST = content

    resultDICT = {}
    if contentLIST:
        if splitLIST:
            # 依 splitLIST 做分句切割
            splitPAT = re.compile("[{}]".format("".join(splitLIST)))
            inputLIST = []
            for c in contentLIST:
                tmpLIST = splitPAT.split(c)
                inputLIST.extend(tmpLIST)
            # 去除空字串
            while "" in inputLIST:
                inputLIST.remove("")
        else:
            # 不做分句切割處理
            inputLIST = contentLIST

        # 依 INPUT_LIMIT 限制批次處理
        for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
            lokiResultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)
            if "msg" in lokiResultDICT:
                return lokiResultDICT

            # 將 lokiResultDICT 結果儲存至 resultDICT
            for k in lokiResultDICT:
                if k not in resultDICT:
                    resultDICT[k] = []
                resultDICT[k].extend(lokiResultDICT[k])

    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)

    if "msg" in resultDICT:
        print(resultDICT["msg"])

def testIntent():
    # AML
    print("[TEST] AML")
    inputLIST = ['廖志傑任職於該公司','記者鄧木卿台中報導','廖佑安係S公司負責人','戴友德為F公司負責人','彭國盛因恐炒股資金不足','毛頌恩為貿易公司負責人','以WhatsApp向汪利行等人詢價','李進杰係某政府機關秘書長','何奕安並自備熱敏票據打印機','使用蔡宏安本人及多個向員工','後張育民於未經董事會同意下','林建國先生與男子高宏貴合作','尹德昌與汪曉明等人無預警失聯','姚仁傑與潘志安二人為牟取不法利益','並由毛頌恩負責在越南進貨與報關事宜','供何奕安黏貼於廉價化粧品及保養品上','吳定國先後於彰化縣及臺中市多個處所','高進安事後將收購訊息透露友人簡尚德','以每月新臺幣3萬5,000元聘僱顧雲淳等8人','或匯款至歐書豪等工作人員名下金融帳戶','誆騙支持者交付現金予毛明政等工作人員','C公司負責人葉曦瑩為逃漏營利事業所得稅','林嘉良受T公司委託製作股權合理性意見書','林建國先生長期無業無法合理交待金錢來源','由林建國出資委託高宏貴於境外自網路黑市','張育民並以H公司員工或友人擔任人頭負責人','何奕安以微信通訊軟體支付人民幣貨款之方式','B公司董事長蔡宏安及總經理王建樹因資金需求','並依葉俊琪指示承租高雄市某址設立S洗錢機房','使用葉俊琪提供之大陸地區人頭金融帳戶與U盾','向有意投標之N公司實際負責人蔡明德索取回扣','馬怡貞與白品良以境外D集團臺灣區負責人名義','黎仁湘於109年間加入年籍不詳B成立之犯罪集團','簡尚德與潘慧萍及潘慧怡等人於重大訊息公告前','復向Y證券公司營業員兼市場金主簡裕民商借資金','總計蔡宏安與彭國盛等人共使用32人87個證券帳戶','事後向蔡明德收取約定之回扣共計新臺幣3,950萬元','吳定國委由不知情之第三方支付公司為代收收款方','復由汪利行透過何燦得指示潘念慈以網路轉帳方式','何奕安再以事先購買之外勞卡門號登入蝦皮人頭帳號','經執法機關查獲該127公克大麻郵包並循線逮捕林建國','尹德昌與汪曉明即自行或指示員工提領R集團帳戶款項','T公司董事杜立賓及S公司董事高進安實際參與洽談過程','另於林建國租用之銀行保險箱內扣得新臺幣960萬元現金','支付款項予歐建豪與江宗發等人申辦臺偽政府發行證件','由汪利行參考當日金融機構人民幣牌告匯率加計2%利潤後','廖灝汶與廖灝俐各於臉書經營社團販賣越南香菸及肉製品','廖灝汶與廖灝俐負責在臺接貨及轉運貨品予在臺購貨客戶','林嘉良配偶潘慧萍及胞妹潘慧怡於林嘉良閒聊中得悉此事','汪利行指示沈宗德與林照山以每戶新臺幣1萬5,000元起價格','馬怡貞與白品良等人非法吸金金額累計達新臺幣65億4,472萬餘元','另由不知情之物流公司在臺報關接貨及送貨至毛頌恩承租之倉庫','改由起訴前消防署長黃季敏涉貪的殺手級檢察官黃珮瑜接手偵辦','曾國琳與林力達與何友山及王呈蓮於103年間共同發起與主持操縱','簡裕民並提供本人及友人證券帳戶配合彭國盛指示價量下單交易','在P確認收到客戶匯入汪利行等人收購之大陸地區金融帳戶款項後','再以國際航空郵件包裏方式將該大麻郵包郵寄至林建國臺北市住處','毛頌恩並雇用員工協助包裝進口轉運貨品供物流業者送交購貨客戶','與股市作手彭國盛以彭國盛本人及彭國盛親友譚永立等人證券帳戶','嚴政蘭指示親屬或以每人新臺幣15萬元至60萬元尋找人頭公司負責人','蔡宏安為維持B公司股價避免遭銀行提徵擔保品與追繳或股票遭斷頭','歐建豪與江宗發等人杜撰渠等成立之臺偽政府已獲美國軍事政府承認','或匯款至歐建豪與江宗發實際控制之臺偽政府基金會境外金融機構帳戶','歐建豪與江宗發等人又以辦理臺偽政府代訓政務人員相關職務訓練課程','H公司負責人張育民於模里西斯與美國與香港及汶萊等地設立G等境外公司','汪利行即命曹世達等人以面交方式支付前揭約定數額之新臺幣現金予客戶','又於林建國住處查扣毒品大麻139公克與販賣大麻資料及新臺幣24萬7,000元現金','毛頌恩與廖志傑與廖灝汶等人於110年8月間透過於空運併袋貨中私運夾藏方式','由尹德昌與汪曉明持不實交易文件陸續向國內銀行申辦應收帳款融資及外銷放款','汪利行即指派曹世達等人向客戶收取新臺幣現金並取得客戶指定匯入之大陸地區帳戶','張育民擅自陸續將G等人頭公司帳戶內總計3億餘元款項匯往L掌控之境外法人帳戶侵占入己','姚仁傑以其擔任負責人之W公司名義將該等夾藏毒品之鉛酸電池由臺灣出口至澳洲或自巴西經美國與臺灣轉運至澳洲','R集團負責人尹德昌與汪曉明指示員工勾結E等合作廠商員工偽造不實買賣合約書與統一發票與出貨單及海運提單等文件']
    testLoki(inputLIST, ['AML'])
    print("")

    # Innocent
    print("[TEST] Innocent")
    inputLIST = ['記者鄧木卿台中報導','檢察官黃珮瑜接手偵辦']
    testLoki(inputLIST, ['Innocent'])
    print("")


if __name__ == "__main__":
    # 測試所有意圖
    #testIntent()

    # 測試其它句子
    filterLIST = []
    #splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";"]
    #resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST)            # output => ["今天天氣"]
    #resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST, splitLIST) # output => ["今天天氣", "後天氣象"]
    #resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"], filterLIST)      # output => ["今天天氣", "後天氣象"]
    resultDICT = execLoki(["彭國盛因恐炒房資金不足"])
    print(resultDICT)
