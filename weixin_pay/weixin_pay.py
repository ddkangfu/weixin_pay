# -*- coding=utf-8 -*-

#from hashcompat import md5_constructor as md5
#from api import random_str, build_mysign, params_to_string
#import requests
import hashlib

from utils import smart_str, dict_to_xml, calculate_sign, random_str, post_xml


class WeixinPay:
    def __init__(self, appid, mch_id, auth_key):
        self.appid = appid
        self.mch_id = mch_id
        self.auth_key = auth_key
        self.comm_params = {
                       "appid": self.appid,
                       "mch_id": self.mch_id,
                      }

    def post_unified_order(self, body, attach, out_trade_no, notify_url, product_id, total_fee):
        """发送预支付单"""
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        unified_order_params = {
                                "nonce_str": "wzgf96zp0qj8az4h9983k9uuwzwqgy7u",
                                "body": smart_str(body),
                                #"attach": attach,
                                "out_trade_no": out_trade_no,
                                "total_fee": total_fee, #以分为单位，为一个字符串整数
                                "spbill_create_ip": '127.0.0.1',
                                "notify_url": notify_url,
                                "trade_type": "NATIVE",
                                #"product_id": product_id,
                                }
        unified_order_params.update(self.comm_params)
        sign = calculate_sign(unified_order_params, self.auth_key)
        xml = dict_to_xml(unified_order_params, sign)
        print xml
        response = post_xml(url, xml)
        print '*' * 5, response.text


if __name__ == "__main__":
    pay = WeixinPay("your_app_id", "your_mch_id", "your_auth_key")
    pay.post_unified_order("贡献一分钱", "bbb", "wx983e4a34aa76e3c41416107999", "http://www.xxxxxx.com/demo/notify_url.php", "1234", "1")
