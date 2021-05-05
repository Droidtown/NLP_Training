#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from ArticutAPI import Articut
from pprint import pprint


if __name__ == "__main__":
    username = "peter.w@droidtown.co"
    apikey   = "pEWjfx317g!zhLnU6W^hnWeyirr&JR6"

    articut = Articut(username, apikey)

    inputSTR = "小紅帽"
    resultDICT = articut.parse(inputSTR, level="lv1") #注意 level 參數設定為 "lv1"
    print("\n lv1 的設定下，處理結果：\n", resultDICT)

    resultDICT = articut.parse(inputSTR, level="lv2") #注意 level 參數設定為 "lv2"
    print("\n lv2 的設定下，處理結果：\n", resultDICT)