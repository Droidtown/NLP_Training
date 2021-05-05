#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from ArticutAPI import Articut
from pprint import pprint


if __name__ == "__main__":
    username = "peter.w@droidtown.co"
    apikey   = "pEWjfx317g!zhLnU6W^hnWeyirr&JR6"

    articut = Articut(username, apikey)

    inputSTR = "會被大家盯上，才證明你有實力"
    resultDICT = articut.parse(inputSTR)
    pprint(resultDICT)