# -*- coding: utf-8 -*-
# @File  : baidu.py
# @Author: ggy
# @Date  : 2019/10/5
# @Software: PyCharm
from setting import SPEECH, VOICE, CHATS_PATH
from uuid import uuid4
import os
from setting import MONGO_DB
from bson import ObjectId
from ai.to_tuling import tuling

def text2audio(text):
    filename = f"{uuid4()}.mp3"
    result = SPEECH.synthesis(text, 'zh', 1,VOICE)
    file_path = os.path.join(CHATS_PATH,filename)

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(file_path, 'wb') as f:
            f.write(result)

    return filename


def get_file_content(filePath):
    os.system(f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()


def audio2text(filepath):
    # 识别本地文件
    res = SPEECH.asr(get_file_content(filepath), 'pcm', 16000, {
        'dev_pid': 1536,
    })

    print(res.get("result")[0])

    return res.get("result")[0]


def my_nlp_lowB(Q, nid):
    # Q = 我要给爸爸发消息
    if "发消息" in Q:
        toy = MONGO_DB.toys.find_one({"_id": ObjectId(nid)})
        for friend in toy.get("friend_list"):
            if friend.get("friend_nick") in Q or friend.get("friend_name") in Q:
                xs = f"可以按消息键给{friend.get('friend_nick')}发消息了"
                filename = text2audio(xs)
                return {"chat": filename, "from_user": str(friend.get("friend_id"))}

    # Ｑ = 我要听 ， 我想听， 播放
    if "我要听" in Q or "我想听" in Q or "播放" in Q:
        content_list = MONGO_DB.content.find({})
        for content in content_list:
            if content.get("title") in Q:
                return {"music": content.get("audio"), "from_user": "ai"}

    text = tuling(Q, nid)
    filename = text2audio(text)

    return  {"chat": filename, "from_user": "ai"}
