# -*- coding: utf-8 -*-
# @File  : caiji.py
# @Author: ggy
# @Date  : 2019/9/28
# @Software: PyCharm
import requests, time
import os
from uuid import uuid4
from setting import MONGO_DB, MUSIC_PATH, IMAGE_PATH

url = "https://m.ximalaya.com/mobile/v1/track/share/content?trackId=%s&tpName=weixin&device=h5"

content_list = ["7713665", "7713762", "7713760", "7713756", "7713682", "7713679", "7713660", "7713655"]
def get_erge(content_list):

    content_list1 = []
    for item in content_list:
        res = requests.get(url % (item))
        res_dict = res.json()

        filename = uuid4()
        audio = requests.get(res_dict.get("audioUrl"))
        pic = requests.get(res_dict.get("picUrl"))
        image = os.path.join(IMAGE_PATH, f"{filename}.jpg")
        music = os.path.join(MUSIC_PATH, f"{filename}.mp3")

        with open(music, "wb") as f:
            f.write(audio.content)

        with open(image, "wb") as f:
            f.write(pic.content)


        muisc_info = {
            "title": res_dict.get("title"),
            "pic": f"{filename}.jpg",
            "audio": f"{filename}.mp3",
        }
        print("下载完成", res_dict.get("title"))
        content_list1.append(muisc_info)
        time.sleep(1)

    MONGO_DB.content.insert_many(content_list1)

get_erge(content_list)
