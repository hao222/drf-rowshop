
# 用于发送短信接口

import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【在线超市】 你的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url, data=parmas)
        import json
        re_dict = json.loads(response.text)
        print(re_dict)
        return re_dict


if __name__ == "__main__":
    yp = YunPian("4f50ae2bdef057fe764d58fd1c484bdf")
    yp.send_sms("2019", "15690711071")