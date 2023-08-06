# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : 小易
# @File : main.py
# @Project : stu
import itertools


case_list = ['用户名', '密码']
value_list = ['正确', '不正确', '特殊符号', '超过最大长度']

def gun_case(item=case_list,value=value_list):
    '''输出迪尔卡用例集合'''
    for i in itertools.product(item,value):
        print("输入".join(i))

def print_multiple(n):
    '''打印乘法表的函数'''
    for i in range(n):
        for j in range(i+1):
            print("%d * %d = %2d"% ((j + 1) , (i + 1) , (j + 1)* (i + 1)), end='  ')