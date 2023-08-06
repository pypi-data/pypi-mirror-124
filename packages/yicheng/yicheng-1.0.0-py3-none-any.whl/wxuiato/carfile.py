# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : 小易
# @File : carfile.py
# @Project : stu
import minium
class FirstTest(minium.MiniTest):
    def test_get_system_info(self):
        sys_info = self.mini.get_system_info()
        self.assertIn("SDKVersion",sys_info)

test = FirstTest()
test.test_get_system_info()