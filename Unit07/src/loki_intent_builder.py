#!/usr/bin/env python3
# -*- coding:utf-8 -*-

try:
    import rapidjson as json
except ModuleNotFoundError:
    import json

import re

from ArticutAPI import Articut
from pprint import pprint
from requests import post
from time import sleep

def utteranceBuilder(payloadDICT):
    url = "https://api.droidtown.co/Loki/Command/"

    for i in range(0, len(payloadDICT["utterance"]), 20):
        payload = {
            "username" : payloadDICT["username"],
            "loki_key" : payloadDICT["loki_key"],
            "intent"   : payloadDICT["intent"],
            "utterance": payloadDICT["utterance"][i:i+20]
        }
        response = post(url, json=payload).json()
        if response["status"] == True:
            sleep(0.5)
        else:
            return response["msg"]
    return response

if __name__== "__main__":
    username    = "peter.w@droidtown.co"
    articut_key = "Jp$Jnnh1KCGEmHvzJ3wmiCXoA4nraNp"
    loki_key    = "aYgqQ%4VRW-vU&SBn@lc^I@#sylXxrh"

    articut = Articut(username=username, apikey=articut_key)
    purgePat = re.compile("</?[a-zA-Z]+?(_[a-zA-Z]+?)?>")

    intentSTR = "AML"
    with open("../corpus/{}_News.json".format(intentSTR), encoding="utf-8") as f:
        amlNewsLIST = json.load(f)

    GoldLIST = []
    toAddUtteranceLIST = []
    for i in amlNewsLIST:
        resultDICT = articut.parse(i.replace("、", "與"))
        for s in resultDICT["result_pos"]:
            if len(s) <= 1:
                pass
            else:
                if "<ENTITY_person>" in s:
                    GoldLIST.extend(re.findall("(?<=<ENTITY_person>)[^<]+?(?=</ENTITY_person>)", s))
                    toAddUtteranceLIST.append("及".join(re.sub(purgePat, "", s).split("及")[:2]))
                else:
                    pass
    print(toAddUtteranceLIST)
    print(GoldLIST)
    payloadDICT = {
        "username" : username,
        "loki_key" : loki_key,
        "intent"   : intentSTR,
        "utterance": toAddUtteranceLIST
    }
    buildResult = utteranceBuilder(payloadDICT)
    print("Intent {} 上傳結果：{}".format(intentSTR, buildResult))


    intentSTR = "Other"
    with open("../corpus/{}_News.json".format(intentSTR), encoding="utf-8") as f:
        amlNewsLIST = json.load(f)

    GoldLIST = []
    toAddUtteranceLIST = []
    for i in amlNewsLIST:
        resultDICT = articut.parse(i.replace("、", "與"))
        for s in resultDICT["result_pos"]:
            if len(s) <= 1:
                pass
            else:
                if "<ENTITY_person>" in s:
                    GoldLIST.extend(re.findall("(?<=<ENTITY_person>)[^<]+?(?=</ENTITY_person>)", s))
                    toAddUtteranceLIST.append("及".join(re.sub(purgePat, "", s).split("及")[:2]))
                else:
                    pass
    print(toAddUtteranceLIST)
    print(GoldLIST)
    payloadDICT = {
        "username" : username,
        "loki_key" : loki_key,
        "intent"   : intentSTR,
        "utterance": toAddUtteranceLIST
    }
    buildResult = utteranceBuilder(payloadDICT)
    print("Intent {} 上傳結果：{}".format(intentSTR, buildResult))