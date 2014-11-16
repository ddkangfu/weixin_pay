# -*- coding=utf-8 -*-

import unittest
import hashlib

from utils import dict_to_xml, calculate_sign, random_str, smart_str
from local_settings import appid, mch_id, auth_key


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


if __name__ == "__main__":
    unittest.main()
