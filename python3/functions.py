#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: functions.py
# Created Date: 2018-06-03 8:34:18
# Author: canalStar
# -----
# Last Modified: 2018-06-04 2:15:45
# Last Modified By: canalStar
###

import requests
import re
from bs4 import BeautifulSoup as BS

def requests_get(ip,user_timeout=1):
    """ 使用get方式进行请求，若连接异常则进行相应报错
    输入参数：ip地址，若没有则默认为登陆ip, 超时时间
    返回值：Response类型对象
    """
    try:
        response = requests.get(ip, timeout=user_timeout)
    except requests.exceptions.Timeout:
        print("连接超时，请检查你的网络连接")
    except :
        print("连接异常，请检查后重试")
    return response

def requests_post(ip, post_data):
    """使用post方式进行请求，若连接异常则进行相应报错
    输入参数：ip地址，默认为登陆ip;post数据
    返回值：Response类型对象
    """
    try:
        response = requests.post(ip, data = post_data)
    except :
        print("连接异常，请检查后重试")
    return response

def get_title(response):
    """解析网页获取title
        输入：Response类型对象
        返回：str类型对象，title及返回也script标签下的内容
    """
    soup = BS(response.text, features='lxml')
    title = soup.title.get_text()
    script_text = soup.script.get_text()
    return title,script_text
    
def disp_local_ip(script_text):
    """解析网页获取并显示本地ip
        输入：Response类型
        输出：空
    """
    local_ip = re.search(r'v46ip=\'(10\.[\d|\.]+)\'',script_text).group(1)
    print("本地IP是：",local_ip)

def display_info(script_text):
    """ 显示上网时长、流量、余额信息
        输入：str
        返回：空
    """
    #时间
    time = re.search(r'time=\'(\d+)\s+\';',script_text).group(1)
    time = int(time)
    if time < 60:
        print("已使用时间 Used time:", time, "Min")
    else:
        print("已使用时间 Used time:%d Hour  %d Min"%(time//60,time%60))
    #流量
    flow = re.search(r'flow=\'(\d+)\s+\';',script_text).group(1)
    flow = int(flow)
    if flow < 1024:
        print("已使用校外流量 Used internet traffic: %d KByte"%(flow))
    elif flow < 1024*1024:
        print("已使用校外流量 Used internet traffic: %.3f MByte"%(flow/1024))
    else:
        print("已使用校外流量 Used internet traffic: %.3f GByte"%(flow/1024/1024))    
    
    #余额
    fee = re.search(r'fsele=1;fee=\'(\d+)\s+\';',script_text).group(1)  
    print("余额 Balance:", int(fee)/10000, "RMB")

def login_error(script_text):
    """若没有登录成功，则根据返回的信息判断是何种问题
        输入：str，登录时返回网页的script标签信息
        返回：空
    """
    return_msg = re.search(r'Msg=(\d\d);', script_text).group(1)
    #用字典进行switch case
    case_dict = {
        '01': '用户名或密码错误',
        '02': '账号正在其他机器使用',
        '04': '余额不足'
    }
    if return_msg in case_dict:
        print(case_dict[return_msg])
    else:
        print("暂不能解析的返回信息代码，请重试")