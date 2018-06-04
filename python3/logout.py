#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: logout.py
# Created Date: 2018-06-04 1:27:17
# Author: canalStar
# -----
# Last Modified: 2018-06-04 2:19:05
# Last Modified By: canalStar
###
import re
import functions

LOGOUT_ADDR = 'http://10.3.8.211/F.htm'  #注销ip地址
user_timeout = 1  #设置连接超时时间，单位为s

def main():
    """ 注销登陆，返回注销是否成功，并显示流量时长等信息
        输入为空或用户名、密码
        返回为空
    """
    response = functions.requests_get(LOGOUT_ADDR, user_timeout)
    title,script_text = functions.get_title(response)
    return_msg = re.search(r'Msg=(\d\d);', script_text).group(1)
    if title == "信息返回窗" and return_msg == '14':
        print("注销成功")
        functions.display_info(script_text)
    else:
        print("注销失败")


if __name__ == '__main__':
    main() 