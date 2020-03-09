# -*- coding: utf-8 -*-
# @File  : setting.py
# @Author: ggy
# @Date  : 2019/9/28
# @Software: PyCharm

import pymongo
from redis import Redis
from aip import AipSpeech, AipNlp

MUSIC_PATH = "Music"
IMAGE_PATH = "Image"
CHATS_PATH = "Chats"
QRCODE_PATH = "QRcode"

# 数据库配置
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
MONGO_DB = client["chunsheng"]

REDIS_DB = Redis(host="127.0.0.1",port=6379, db=10)

# Rest-Api
RET = {
    "code": 0,
    "msg": "",
    "data": {}
}


# 二维码配置：
LT_URL = "http://qr.topscan.com/api.php?text=%s"


# baiduAi 配置
""" 你的 APPID AK SK """
APP_ID = '17358838'
API_KEY = '0HsMMtyfVbHGi8E0lvHkEsNG'
SECRET_KEY = 'Ax2Sfx7dWnP4PD1FNYY6vT8UNKNbzmYy'

NLP = AipNlp(APP_ID, API_KEY, SECRET_KEY)
SPEECH = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

VOICE = {
    'vol': 5,
    "spd": 4,
    "pit": 8,
    "per": 4
}

# 图灵配置
TULING_STR = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": ""
        }
    },
    "userInfo": {
        "apiKey": "9a9a026e2eb64ed6b006ad99d27f6b9e",
        "userId": ""
    }
}

TULING_URL = "http://openapi.tuling123.com/openapi/api/v2"

