# -*- coding: utf-8 -*-
# @File  : to_tuling.py
# @Author: ggy
# @Date  : 2019/10/5
# @Software: PyCharm
from setting import TULING_STR, TULING_URL
import requests

def tuling(Q, nid):
    TULING_STR["perception"]["inputText"]["text"] = Q
    TULING_STR["userInfo"]["userId"] = nid

    res = requests.post(TULING_URL, json=TULING_STR)
    text = res.json().get("results")[0].get("values").get("text")
    print(text)
    return text
