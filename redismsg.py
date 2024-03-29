# -*- coding: utf-8 -*-
# @File  : redismsg.py
# @Author: ggy
# @Date  : 2019/10/5
# @Software: PyCharm
from setting import REDIS_DB
import json


def set_redis(to_user, from_user):
    # toy:{app:2}
    to_user_msg = REDIS_DB.get(to_user)
    if to_user_msg:
        to_user_msg = json.loads(to_user_msg)
        if to_user_msg.get(from_user):
            to_user_msg[from_user] += 1
        else:
            to_user_msg[from_user] = 1

    else:
        to_user_msg = {from_user: 1}

    REDIS_DB.set(to_user, json.dumps(to_user_msg))


def get_redis_one(to_user, from_user):
    to_user_msg = REDIS_DB.get(to_user)
    if to_user_msg:
        to_user_msg = json.loads(to_user_msg)
        count = to_user_msg.get(from_user, 0)

        to_user_msg[from_user] = 0
        REDIS_DB.set(to_user, json.dumps(to_user_msg))
        return count
    else:
        return 0


def get_redis_all(to_user):
    to_user_msg = REDIS_DB.get(to_user)
    if to_user_msg:
        to_user_msg = json.loads(to_user_msg)
        # {"toy": 1, "toy2": 1, "toy3": 2}
        to_user_msg["count"] = sum(to_user_msg.values())

        return to_user_msg
    else:
        return {"count": 0}


