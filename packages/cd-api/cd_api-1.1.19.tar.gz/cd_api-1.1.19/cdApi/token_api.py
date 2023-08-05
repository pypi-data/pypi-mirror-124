"""
@说明    :草动商城管理端取得token
@时间    :2020/3/8 下午6:25:59
@作者    :任秋锴
@版本    :1.0
"""
import requests
import time
import uuid
import numpy as np
from loguru import logger


class Token:
    code_url = ""

    def __init__(self):
        # 初始化
        self.makeCodeUrl()

    def get_image_code(self):
        resp = requests.get(self.code_url)
        url = f"http://cd.renqiukai.com/tool/redis/get_image_code?uuid={self.uuid_str}"
        resp = requests.get(url)
        if resp.status_code == 200:
            image_code = resp.json().get("image_code")
            logger.debug(
                {
                    "image_code": image_code,
                    "uuid_str": self.uuid_str,
                }
            )
            return image_code

    def makeCodeUrl(self):
        # 生成coder的url
        self.uuid_str = str(uuid.uuid4())
        timestamp = time.time()
        self.code_url = f"https://api.icaodong.com/manager/sysuser/imagecode?uuid={self.uuid_str}&time={int(timestamp*100)}"

    def get(self, tenantId: int, acc: str, pwd: str, acc_type: int = 0) -> str:
        """取得token的方法

        Args:
            tenantId (int): [草动租户ID]
            acc (str): [账号]
            pwd (str): [密码]
            acc_type (int, optional): [账号类型，0表示个人管理员1表示企业管理员]. Defaults to 0.

        Returns:
            [str]: [返回token字符串或者None]
        """
        # self.openCode()
        data = {
            "tenantId": tenantId,
            "mobile": acc,
            "password": pwd,
            "code": self.get_image_code(),
            "uuid": self.uuid_str,
            "brandType": "1",
            "type": acc_type,
        }
        url = "https://api.icaodong.com/manager/sysuser/login"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            response_json = response.json()
            status = response_json.get("status")
            if status == 200:
                # 成功
                token = response_json.get("data").get("token")
                logger.success(f"token is {token}")
                return token
            else:
                # 失败
                msg = response_json.get("message")
                logger.error(
                    dict(msg=msg, url=url, data=data, response_json=response_json)
                )
                # 失败重试
                self.get(tenantId=tenantId, acc=acc, pwd=pwd, acc_type=acc_type)


class TokenV2(Token):
    def __init__(self):
        super().__init__()

    def get(self, tenantId: int, acc: str, pwd: str, acc_type: int = 0):
        url = self.makeCodeUrl()


def testcase():
    t = Token()
    t.get(10310, "13801587423", "xtep123456", 1)


if __name__ == "__main__":
    testcase()
