# -*- coding: utf-8 -*-
# @File  : devices.py
# @Author: ggy
# @Date  : 2019/9/29
# @Software: PyCharm
from flask import Blueprint, jsonify, request
from setting import MONGO_DB, RET
from bson import ObjectId

devices = Blueprint("devices", __name__)


@devices.route("/validate_code", methods=["POST"])
def validate_code():
    code = request.form.to_dict()  # {}
    res = MONGO_DB.devices.find_one(code, {"_id": 0})

    if res:
        RET["code"] = 0
        RET["msg"] = "设备已授权，开启绑定流程"
        RET["data"] = res
        # 添加好友逻辑

    else:
        RET["code"] = 2
        RET["msg"] = "非授权设备"
        RET["data"] = res

    return jsonify(RET)


@devices.route("/bind_toy", methods=["POST"])
def bind_toy():
    # toy.bind_user = "user_id"
    # users.bind_toy = ["toy_id]
    # 1. device_key  2. fromdata
    toy_info = request.form.to_dict()

    caht_window = MONGO_DB.chats.insert_one({"user_list": [], "chat_list": []})

    user_info = MONGO_DB.users.find_one({"_id": ObjectId(toy_info["user_id"])})

    toy_info["bind_user"] = toy_info.pop("user_id")
    toy_info["avatar"] = "toy.jpg"
    toy_info["friend_list"] = [
        {
            "friend_id": toy_info["bind_user"],
            "friend_name": user_info.get("nickname"),
            "friend_nick": toy_info.pop("remark"),
            "friend_avatar": user_info.get("avatar"),
            "friend_type": "app",
            "friend_chat": str(caht_window.inserted_id)
        }
    ]

    toy = MONGO_DB.toys.insert_one(toy_info)

    # 用户添加绑定玩具 及 自然逻辑 好友关系
    user_info["bind_toy"].append(str(toy.inserted_id))
    user_add_tot = {
        "friend_id": str(toy.inserted_id),
        "friend_name": toy_info.get("toy_name"),
        "friend_nick": toy_info.pop("baby_name"),
        "friend_avatar": toy_info.get("avatar"),
        "friend_type": "toy",
        "friend_chat": str(caht_window.inserted_id)
    }

    user_info["friend_list"].append(user_add_tot)

    MONGO_DB.users.update_one({"_id": ObjectId(toy_info["bind_user"])}, {"$set": user_info})
    MONGO_DB.chats.update_one(
        {"_id": caht_window.inserted_id},
        {"$set":
             {"user_list": [str(toy.inserted_id), str(user_info.get("_id"))]}
        })

    RET["code"] = 0
    RET["msg"] = "添加玩具成功"
    RET["data"] = {}

    return jsonify(RET)


@devices.route("/toy_list", methods=["POST"])
def toy_list():
    # bind_toy : [Obj("toy_id"), "toy_id2"]

    user_id = request.form.get("user_id")
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    user_bind_toy = user_info.get("bind_toy")

    for index, item in enumerate(user_bind_toy):
        user_bind_toy[index] = ObjectId(item)

    toy_l = list(MONGO_DB.toys.find({"_id": {"$in": user_bind_toy}}))

    for index, toy in enumerate(toy_l):
        toy_l[index]["_id"] = str(toy.get("_id"))

    RET["code"] = 0
    RET["msg"] = "查看所有绑定玩具"
    RET["data"] = toy_l

    return jsonify(RET)


@devices.route("/device_login", methods=["POST"])
def device_login():
    dev_info = request.form.to_dict()
    dev = MONGO_DB.devices.find_one(dev_info)
    # 校验设备 DeviceKey 是否有效
    if dev:
        toy = MONGO_DB.toys.find_one(dev_info)
        # 校验设备 DeviceKey 是否已经成为玩具
        if MONGO_DB.toys.find_one(dev_info):
            return jsonify({"music": "Welcome.mp3", "info": str(toy.get("_id"))})
        return jsonify({"music": "Nobind.mp3"})
    else:
        return jsonify({"music": "Nolic.mp3"})



