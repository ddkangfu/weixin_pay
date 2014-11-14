# -*- coding=utf-8 -*-

#from hashcompat import md5_constructor as md5
from api import random_str, build_mysign, params_to_string
import requests
import hashlib

def pay():
    params = {
              "appid": "wxd930ea5d5a258f4f",
              "auth_code": "123456",
              "body": "test",
              "device_info": "123",
              "mch_id": "1900000109",
              "nonce_str": "960f228109051b9969f76c82bde183ac",
              "out_trade_no": "1400755861",
              "spbill_create_ip": "127.0.0.1",
              "total_fee": "1",
    }
    #sing = build_mysign(params, "h7Jr5z6RDl")
    params_url = params_urlencode(params)
    print params_url
    params_url = '%s&key=%s' % (params_url, smart_str('8934e7d15453e97507ef794cf7b0519d'))
    print params_url
    #sign = md5(params).hexdigest().upper()
    #print sign
    sign = hashlib.md5(params_url).hexdigest().upper()
    print sign
    params["sign"] = sign

    str1 = "appid=wxd930ea5d5a258f4f&auth_code=123456&body=test&device_info=123&mch_id=1900000109&nonce_str=960f228109051b9969f76c82bde183ac&out_trade_no=1400755861&spbill_create_ip=127.0.0.1&total_fee=1&key=8934e7d15453e97507ef794cf7b0519d"
    print hashlib.md5(str1).hexdigest().upper()


    #package = params_to_string(params) + "&sign=" + sign

    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

    #['appid', 'attach', 'body', 'mch_id', 'nonce_str', 'notify_url',
    #'out_trade_no', 'product_id', 'spbill_create_ip', 'time_expire', 'time_start', 'total_fee', 'trade_type']
    post_text = ("<appid>%s</appid><auth_code>%s</auth_code><body><![CDATA[%s]]></body><device_info>%s</device_info><mch_id>%s</mch_id>"
                 "<nonce_str><![CDATA[%s]]></nonce_str><out_trade_no><![CDATA[%s]]></out_trade_no><spbill_create_ip>%s</spbill_create_ip>"
                 "<total_fee>%s</total_fee><sign><![CDATA[%s]]></sign>"
                )%(params['appid'], params['auth_code'], params['body'], params['device_info'], params['mch_id'],
                   params['nonce_str'], params['out_trade_no'], params['spbill_create_ip'], params['total_fee'],
                   '729A68AC3DE268DBD9ADE442382E7B24',
                )

    r = requests.post(url, data=post_text)
    print (r.text)
    #print direct_pay_url
    #return direct_pay_url

def params_urlencode(params):
    keys = params.keys()
    keys.sort()

    print keys

    result = []
    for key in keys:
        value = params[key]
        if value != "":
            result.append('%s=%s' % (key, smart_str(value)))

    return '&'.join(result)


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

if __name__ == "__main__":
    pay()
