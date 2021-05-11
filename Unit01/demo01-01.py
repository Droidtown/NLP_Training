#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from ArticutAPI import Articut
from pprint import pprint


if __name__ == "__main__":
    username = "" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
    apikey   = "" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。

    articut = Articut(username, apikey)

    inputSTR = "會被大家盯上，才證明你有實力"
    resultDICT = articut.parse(inputSTR)
    pprint(resultDICT)