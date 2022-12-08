#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Innocent

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

DEBUG_Innocent = True
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except:
    userDefinedDICT = {}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Innocent:
        print("[Innocent] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[檢察官][黃珮瑜]接手偵辦":
        resultDICT["innocent"].append(args[1])

    if utterance == "[記者][鄧木卿][台中]報導":
        resultDICT["innocent"].append(args[1])

    return resultDICT