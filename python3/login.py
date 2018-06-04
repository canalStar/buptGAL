#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: login.py
# Created Date: 2018-06-04 1:27:06
# Author: canalStar
# -----
# Last Modified: 2018-06-04 1:03:43
# Last Modified By: canalStar
###

""" 登录脚本，若正常登录会显示本地ip，上网时长、流量、账户余额等信息
    登录格式为：
    python login.py [用户名] [密码]
    例如：
    python login.py 200101010101 password
    也可自行更改代码中的 default_userid, default_passwd以便登录时不用每次输入密码
"""


import functions
import sys

LOGIN_ADDR = 'http://10.3.8.211/'  #登录ip地址
user_timeout = 1  #设置默认连接超时时间，单位为s
post_data = {}  #初始化post参数，为字典类型
#！！！！注意：代码发布时将userid,passwd两行删除
default_userid = '2001010101'  #默认用户名
default_passwd = 'password'  #默认密码

def main(argv=None):
    """登陆界面，先获取本地ip，然后登陆，并显示流量时长等信息
        输入：空
        输出：空
    """
    #检查输入
    if argv is None:
        userid = default_userid
        passwd = default_passwd
    elif len(argv) == 1:
        userid = argv[0]
        passwd = default_passwd
    elif len(argv) == 2:
        userid = argv[0]
        passwd = argv[1]
    else:
        print("参数输入错误，请检查！")

    #post数据包
    post_data['DDDDD'] = userid
    post_data['upass'] = passwd
    post_data['0MKKey'] =''

    #检查是否连接成功，若成功，从返回参数中提取ip并显示ip地址
    response = functions.requests_get(LOGIN_ADDR, user_timeout)
    title,script_text = functions.get_title(response)
    
    #若title为'欢迎登录北邮校园网络'说明连接成功，且为登录界面
    if title == '欢迎登录北邮校园网络':
        functions.disp_local_ip(script_text)
        #连接成功后进行登录
        response = functions.requests_post(LOGIN_ADDR, post_data)
        #获取title
        title,script_text = functions.get_title(response)
        if title == '登录成功窗':
            print("登陆成功")
            #显示信息
            response = functions.requests_get(LOGIN_ADDR, user_timeout)
            title,script_text = functions.get_title(response)
            functions.display_info(script_text)
        elif title == '信息返回窗':
            functions.login_error(script_text)
        else:
            print("未知登陆错误，请检查并重试")
    #若返回title为上网注销窗，说明已经成功登录
    elif title == "上网注销窗":  
        print("已登陆成功")
    else:
        print("连接出现问题，请重试")  

if __name__ == "__main__":
    #sys.argv至少有一个参数，若只有一个参数则用户没有传递参数
    if len(sys.argv) == 1:
        main()
    else:
        args = sys.argv[1:]
        main(args)