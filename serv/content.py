# -*- coding: utf-8 -*-
# @File  : content.py
# @Author: ggy
# @Date  : 2019/9/28
# @Software: PyCharm
from flask import Blueprint, jsonify
from setting import MONGO_DB, RET

content = Blueprint("content", __name__)


@content.route("/content_list", methods=["POST"])
def content_list():
    res = list(MONGO_DB.content.find({}))

    for index, item in enumerate(res):
        res[index]["_id"] = str(item.get("_id"))

    RET["code"] = 0
    RET["msg"] = "查询幼教内容"
    RET["data"] = res

    return jsonify(RET)