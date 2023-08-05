'''
制作时间：2021/10/19
作者：PYmili
系统：windows 10 专业版
Python版本：3.9.7
'''
import random

"""
key 随机生成一串秘钥
key(number=生成位数。必须为整数)
生成类型有：0123456789qwertyuiopasdfghjklzxcvbnm
返回一个字符串
"""

def key(number):
    num = "1234567890qwertyuiopasdfghjklzxcvbnm" # 生成类型
    num_list = []
    for i in range(int(number)):
        and_num = random.choice(num)
        num_list.append(and_num)
    key = ''.join(num_list)
    return key

"""
keyint 随机生成一串秘钥
keyint(number=生成位数。必须为整数)
生成包含：1234567890
返回一个整数
"""

def keyint(number):
    int_list = []
    for i in range(int(number)):
        num = random.randint(0, 9)
        int_list.append(f'{num}')
    key = ''.join(int_list)
    return int(key)
