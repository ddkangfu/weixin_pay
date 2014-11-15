# -*- coding=utf-8 -*-

import unittest


class TestUtils(unittest.TestCase):
    #def test_calculate_sign(self):
    #    pass

    def test_dict_to_xml(self):
        params = {"123": "123"}
        result = dict_to_xml(params)
        expect_result = "<xml><123>123</123></xml>"
        self.assertEqual(result, expect_result)

        params = {"123": "xyz123"}
        result = dict_to_xml(params)
        expect_result = "<xml><123><![DATA[xyz123]]></123></xml>"
        self.assertEqual(result, expect_result)

        params = {"abc": "abc", "123": "123"}
        result = dict_to_xml(params)
        expect_result = "<xml><123>123</123><abc><![DATA[abc]]></abc></xml>"
        self.assertEqual(result, expect_result)

