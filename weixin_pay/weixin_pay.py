# -*- coding=utf-8 -*-

import hashlib

from utils import (smart_str, dict_to_xml, calculate_sign, random_str,
    post_xml, xml_to_dict, validate_post_xml, format_url)
#from local_settings import appid, mch_id, api_key


class WeiXinPay(object):
    def __init__(self, appid, mch_id, api_key):
        self.appid = appid #微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
        self.mch_id = mch_id #受理商ID，身份标识
        self.api_key = api_key #商户支付密钥Key。审核通过后，在微信发送的邮件中查看
        self.common_params = {
                              "appid": self.appid,
                              "mch_id": self.mch_id,
                             }
        self.params = {}
        self.url = ""
        self.trade_type = ""

    def set_params(self, **kwargs):
        self.params = {}
        for (k, v) in kwargs.items():
            self.params[k] = smart_str(v)

        self.params["nonce_str"] = random_str(32)
        self.params["trade_type"] = self.trade_type
        self.params.update(self.common_params)

    def post_xml(self):
        sign = calculate_sign(self.params, self.api_key)
        xml = dict_to_xml(self.params, sign)
        response = post_xml(self.url, xml)
        return xml_to_dict(response.text)

    def valiate_xml(self, xml):
        return validate_post_xml(xml)

    def get_error_code_desc(self, error_code):
        error_desc = {
                      "SYSTEMERROR": u"接口后台错误",
                      "INVALID_TRANSACTIONID": u"无效 transaction_id",
                      "PARAM_ERROR": u"提交参数错误",
                      "ORDERPAID": u"订单已支付",
                      "OUT_TRADE_NO_USED": u"商户订单号重复",
                      "NOAUTH": u"商户无权限",
                      "NOTENOUGH": u"余额丌足",
                      "NOTSUPORTCARD": u"不支持卡类型",
                      "ORDERCLOSED": u"订单已关闭",
                      "BANKERROR": u"银行系统异常",
                      "REFUND_FEE_INVALID": u"退款金额大亍支付金额",
                      "ORDERNOTEXIST": u"订单不存在",
        }
        return error_desc.get(error_code.strip().upper(), u"未知错误")


class UnifiedOrderPay(WeiXinPay):
    """发送预支付单"""
    def __init__(self, appid, mch_id, api_key):
        super(UnifiedOrderPay, self).__init__(appid, mch_id, api_key)
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.trade_type = "NATIVE"
        
    def post(self, body, out_trade_no, total_fee, spbill_create_ip, notify_url):
        kwargs = {
                  "body": body,
                  "out_trade_no": out_trade_no,
                  "total_fee": total_fee,
                  "spbill_create_ip": spbill_create_ip,
                  "notify_url": notify_url,
                 } 
        self.set_params(**kwargs)
        return self.post_xml()


class OrderQuery(WeiXinPay):
    """订单状态查询"""
    def __init__(self, appid, mch_id, api_key):
        super(OrderQuery, self).__init__(appid, mch_id, api_key)
        self.url = "https://api.mch.weixin.qq.com/pay/orderquery"

    def post(self, out_trade_no):
        self.set_params(out_trade_no=out_trade_no)
        return self.post_xml()


class JsAPIOrderPay(WeiXinPay):
    def __init__(sefl, appid, mch_id, api_key, app_secret):
        super(JsAPIOrderPay, self).__init__(appid, mch_id, api_key)
        self.app_secret = app_secret

    def create_oauth_url_for_code(self, redirect_uri):
        url_params = {
                      "appid": self.appid,
                      "redirect_uri": redirect_uri,
                      "response_type": "code",
                      "scope": "snsapi_base",
                      "state": "STATE#wechat_redirect"
                     }
        url = format_url(url_params)
        return "https://open.weixin.qq.com/connect/oauth2/authorize?%s" %url

    def _create_oauth_url_for_openid(self, code):
        url_params = {
                      "appid": self.appid,
                      "secret": self.app_secret,
                      "code": code,
                      "grant_type": "authorization_code",
                      }
        url = format_url(url_params)
        return "https://api.weixin.qq.com/sns/oauth2/access_token?%s" % url

    def get_openid(self, code):
        url = self._create_oauth_url_for_openid(code)
        #TODO:需要确定请求后返回的数据格式，再进一步解析得到openid
        return requests.get(url)


#if __name__ == "__main__":
#    pay = UnifiedOrderPay(appid, mch_id, api_key)
    #pay.post_unified_order("贡献一分钱", "wx983e4a34aa76e3c41416107999", "http://www.xxxxxx.com/demo/notify_url.php", "1")
#    print pay.post(body="贡献一分钱", out_trade_no="wx983e4a34aa76e3c41416149262", total_fee="1",
#            spbill_create_ip="127.0.0.1", notify_url="http://www.xxxxxx.com/demo/notify_url.php")
    #print pay.post()
