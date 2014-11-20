# -*- coding=utf-8 -*-

import unittest
import hashlib

from utils import dict_to_xml, calculate_sign, random_str, smart_str, xml_to_dict
from local_settings import appid, mch_id, api_key


class TestUtils(unittest.TestCase):
    def test_calculate_sign(self):
        params = {"123": "123"}
        key = "12345678901234567890"
        sign = calculate_sign(params, key)
        expect_sign = hashlib.md5("123=123&key=%s"%key).hexdigest().upper()
        self.assertEqual(sign, expect_sign)

        params = {"abc": "abc", "123": "123"}
        sign = calculate_sign(params, key)
        expect_sign = hashlib.md5("123=123&abc=abc&key=%s" % key).hexdigest().upper()
        print sign
        self.assertEqual(sign, expect_sign)


    def test_dict_to_xml(self):
        params = {"123": "123"}
        sign = '1234567890'
        result = dict_to_xml(params, sign)
        expect_result = "<xml><123>123</123><sign><![CDATA[%s]]></sign></xml>" % sign
        self.assertEqual(result, expect_result)

        params = {"123": "xyz123"}
        result = dict_to_xml(params, sign)
        expect_result = "<xml><123><![CDATA[xyz123]]></123><sign><![CDATA[%s]]></sign></xml>" % sign
        self.assertEqual(result, expect_result)

        #params = {"abc": "abc", "123": "123"}
        params = {"123": "123", "abc": "abc", }
        result = dict_to_xml(params, sign)
        expect_result = "<xml><123>123</123><abc><![CDATA[abc]]></abc><sign><![CDATA[%s]]></sign></xml>" % sign
        self.assertEqual(result, expect_result)

        params = {"c": "123", "a": "abc", }
        result = dict_to_xml(params, sign)
        expect_result = "<xml><a><![CDATA[abc]]></a><c>123</c><sign><![CDATA[%s]]></sign></xml>" % sign
        self.assertEqual(result, expect_result)


    def test_random_str(self):
        result = random_str()
        print result
        self.assertEqual(len(result), 8)

        result = random_str(32)
        print result
        self.assertEqual(len(result), 32)


    def test_xml_to_dict(self):
        xml = "<a>xxx</a>"
        sign, result = xml_to_dict(xml)
        self.assertEqual(sign, None)
        self.assertEqual(result, None)

        xml = "<xml><a>xxx</a></xml>"
        sign, result = xml_to_dict(xml)
        self.assertEqual(sign, None)
        self.assertEqual(len(result), 1)
        self.assertEqual(result["a"], "xxx")

        xml = "<xml><a>xxx</a><b>yyy</b></xml>"
        sign, result = xml_to_dict(xml)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["a"], "xxx")
        self.assertEqual(result["b"], "yyy")

        xml = "<xml><a>xxx</a><b>yyy</b><c><![CDATA[zzz]]></c></xml>"
        sign, result = xml_to_dict(xml)
        self.assertEqual(len(result), 3)
        self.assertEqual(result["a"], "xxx")
        self.assertEqual(result["b"], "yyy")
        self.assertEqual(result["c"], "zzz")

        xml = """<xml><return_code><![CDATA[SUCCESS]]></return_code>
<return_msg><![CDATA[OK]]></return_msg>
<appid><![CDATA[wx12233445566778899]]></appid>
<mch_id><![CDATA[12345678]]></mch_id>
<nonce_str><![CDATA[Sv9ATOOBtYWvtUQs]]></nonce_str>
<sign><![CDATA[0C638718BE0316E9B16E57DC869D2CD1]]></sign>
<result_code><![CDATA[SUCCESS]]></result_code>
<prepay_id><![CDATA[wx20141117135919f494cdaadb0287308957]]></prepay_id>
<trade_type><![CDATA[NATIVE]]></trade_type>
<device_info><![CDATA[]]></device_info>
<code_url><![CDATA[weixin://wxpay/bizpayurl?sr=GnZnlWr]]></code_url></xml>"""
        
        sign, result = xml_to_dict(xml)
        print result
        self.assertEqual(sign, "0C638718BE0316E9B16E57DC869D2CD1")
        self.assertEqual(len(result), 9)
        self.assertEqual(result["return_code"], "SUCCESS")
        self.assertEqual(result["return_msg"], "OK")
        self.assertEqual(result["result_code"], "SUCCESS")
        self.assertEqual(result["code_url"], "weixin://wxpay/bizpayurl?sr=GnZnlWr")
        self.assertEqual(result.get("device_info", None), None)
        

if __name__ == "__main__":
    unittest.main()
