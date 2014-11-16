# -*- coding=utf-8 -*-

import hashlib

from utils import smart_str, dict_to_xml, calculate_sign, random_str, post_xml
from local_settings import appid, mch_id, auth_key


class WeiXinBasePay(object):
    def __init__(self, appid, mch_id, auth_key):
        self.appid = appid #微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
        self.mch_id = mch_id #受理商ID，身份标识
        self.auth_key = auth_key #商户支付密钥Key。审核通过后，在微信发送的邮件中查看
        self.common_params = {
                              "appid": self.appid,
                              "mch_id": self.mch_id,
                             }
        self.params = {}
        self.url = ""
        self.trade_type = ""

    def set_params(self, **kwags):
        self.params = {}
        for (k, v) in kwags.items():
            self.params[k] = smart_str(v)

        self.params["nonce_str"] = random_str(32)
        self.params["trade_type"] = self.trade_type
        self.params.update(self.common_params)

    def post_xml(self):
        sign = calculate_sign(self.params, self.auth_key)
        xml = dict_to_xml(self.params, sign)
        print xml
        response = post_xml(self.url, xml)
        print '*' * 5, response.text
        return response


class UnifiedOrderPay(WeiXinBasePay):
    """发送预支付单"""
    def __init__(self, appid, mch_id, auth_key):
        super(UnifiedOrderPay, self).__init__(appid, mch_id, auth_key)
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.trade_type = "NATIVE"

    #def post_xml(self, body, out_trade_no, total_fee, spbill_create_ip, notify_url):
    #    self.params["body"] = smart_str(body)
    #    self.params["out_trade_no"] = out_trade_no
    #    self.params["total_fee"] = total_fee
    #    self.params["spbill_create_ip"] = spbill_create_ip
    #    self.params["notify_url"] = notify_url
    #    return super(UnifiedOrderPay, self).post_xml()
        

    #def post_unified_order(self, body, out_trade_no, notify_url, total_fee):
    #    """发送预支付单"""
    #    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    #    unified_order_params = {
    #                            "nonce_str": random_str(32),
    #                            "body": smart_str(body),
    #                            "out_trade_no": out_trade_no,
    #                            "total_fee": total_fee, #以分为单位，为一个字符串整数
    #                            "spbill_create_ip": '127.0.0.1',
    #                            "notify_url": notify_url,
    #                            "trade_type": "NATIVE",
    #                            }
    #    unified_order_params.update(self.comm_params)
    #    sign = calculate_sign(unified_order_params, self.auth_key)
    #    xml = dict_to_xml(unified_order_params, sign)
    #    print xml
    #    response = post_xml(url, xml)
    #    print '*' * 5, response.text


if __name__ == "__main__":
    pay = UnifiedOrderPay(appid, mch_id, auth_key)
    #pay.post_unified_order("贡献一分钱", "wx983e4a34aa76e3c41416107999", "http://www.xxxxxx.com/demo/notify_url.php", "1")
    pay.set_params(body="贡献一分钱", out_trade_no="wx983e4a34aa76e3c41416107999", total_fee="1",
            spbill_create_ip="127.0.0.1", notify_url="http://www.xxxxxx.com/demo/notify_url.php")
    print pay.post_xml()
