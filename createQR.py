# -*- coding: utf-8 -*-
# @File  : createQR.py
# @Author: ggy
# @Date  : 2019/9/29
# @Software: PyCharm
import requests, time, hashlib, os
from uuid import uuid4

from setting import LT_URL, QRCODE_PATH, MONGO_DB


def create_QR(count):
    qr_list = []
    for i in range(count):
        qr_code = hashlib.md5(f"{uuid4()}{time.time()}{uuid4()}".encode("utf8")).hexdigest()
        res = requests.get(LT_URL % (qr_code))
        qr_path = os.path.join(QRCODE_PATH, f"{qr_code}.jpg")

        with open(qr_path, "wb") as f:
            f.write(res.content)

        qr_dict = {"device_key": qr_code}
        qr_list.append(qr_dict)
        time.sleep(0.5)

    MONGO_DB.devices.insert_many(qr_list)


create_QR(10)
