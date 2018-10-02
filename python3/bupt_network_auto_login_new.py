#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: school_networ_auto_login_new.py
# Created Date: 2018-10-02 16:07:21
# Author: canalStar
# -----
# Last Modified: 2018-10-03 02:23:22
# Last Modified By: canalStar
"""
    若未安装bs4，需要先安装bs4才可运行
    使用前先更改默认的用户名、密码以及网络提供商
"""

import requests
import re
from bs4 import BeautifulSoup as BS

class BUPTGateway:
    """ 北邮网关登录脚本\n
        有三个函数： 设置用户登录信息 set_user_info(),\n
                    检查是否连接到校园网 check_network(),\n
                    登录网络并返回结果 login()\n
    """

    def __init__(self, login_addr = 'http://10.3.8.217/login', logout_addr = 'http://10.3.8.211/logout', user_timeout = 1):
        """ 构造函数，可以使用默认的参数，也可自己传入参数\n
            传入参数为：登录地址(str),注销地址(str),最大连接时长(int)
        """
        self.login_addr = login_addr
        self.logout_addr = logout_addr
        self.user_timeout = 1  #设置连接超时时间，单位为秒
        self.user_id = ''
        self.passwd = ''
        self.supplier = ''

    def set_user_info(self, userid = '', passwd = '', supplier_choice = 0):
        """ 用户登录的基本信息\n
            输入参数依次为：用户名(str)，密码(str)，网络供应商选择(int)\n
            输出参数为封装好的post字典\n
        """
        #网络供应商列表，依次为校园网，联通，移动，电信
        supplier_list = ['', 'CUC-BRAS', 'CMCC-BRAS', 'CT-BRAS']
        #设置用户信息
        self.userid = userid
        self.passwd = passwd
        self.supplier = supplier_list[supplier_choice]
        self.post_data = {}
        self.post_data['user'] = self.userid
        self.post_data['pass'] = self.passwd
        self.post_data['line'] = self.supplier
        return self.post_data

    def check_network(self):
        """ 网络检查：检查到网关地址的连通性
            输入：空
            输出：若可以连接到网关地址，则返回True，否则返回False
        """
        try:
            response = requests.get(self.login_addr, timeout = self.user_timeout)  #若超时则抛出异常，response为一个response对象
        except requests.exceptions.Timeout:
            print("连接超时，请检查你的网络连接")
        except :
            print("连接异常，请检查后重试")
        #若连接正常，则进行对返回的信息进行解析，若页面title为'网络认证登录'
        else:
            #使用BeautifulSoup进行网页解析
            soup = BS(response.text, features ='lxml')    #封装成bs4对象
            #提取网页title
            title = soup.title.get_text()
            #若该页面是网络登陆页面，则解析出本机ip地址，否则报告错误
            if title == '网络认证登录':   #正常登陆界面的title是“欢迎登录北邮校园网络”
                return True

    def login(self, addr, data):
        """ 登录函数
            输入数据为登录地址(str)，post数据(dict)
            输出：若登录成功，返回True，否则False
        """
        try:
            #使用requests进行post请求，返回的对象是response类型
            response = requests.post(addr, data, timeout = self.user_timeout)
        except requests.exceptions.Timeout:
            print("连接超时，请检查你的网络连接")
        except :
            raise
        else:
            #封装成bs4对象
            soup = BS(response.text, features = 'lxml')
            #对返回页面进行解析，判断是否登录成功，若登录失败，判断是否是“认证失败”错误
            #查找登录成功标记，若登录成功，返回页面中会有值为'login-success'的'class'
            response_label = soup.find_all('div', {'class': 'login-success'})
            if len(response_label) > 0:
                result = self.check_connection_to_baidu()
                if result == 200:
                    print("网关登录成功，连接至外网检测成功")
                else:
                    print("网关登录成功，但连接至外网检测失败，请检查")
            else:
                msg_label = soup.find_all('div', {'class':'ui error message'})
                for tag in msg_label:
                    #判断登录不成功原因是否是因为认证失败
                    msg = re.search('认证失败', tag.text).span()
                    if len(msg) > 0:
                        print("认证失败，请检查您的账号密码或是否存在账号到期及余额不足的情况")
                    else:
                        print("登录失败，请检查")
    
    def check_connection_to_baidu(self):
        """ 在网关登录成功后，通过尝试连接到百度检查是否成功连接至外网\n
            返回值为网络请求返回的状态码
        """
        response = requests.get('http://www.baidu.com/')
        return response.status_code

if __name__ == '__main__':
    login_addr = 'http://10.3.8.217/login'
    logout_addr = 'http://10.3.8.211/logout'

    #手动输入用户名密码
    #userid = input("请输入您的账号:")
    #passwd = input("请输入您的密码:")
    #supplier_choice = eval(input("请选择网络提供商:\n\t 0为校园网;\n\t 1为联通;\n\t 2为移动;\n\t 3为电信;\n"))

    #使用前先更改默认的用户名、密码以及网络提供商
    userid = '更改你的学号'
    passwd = '更改你的密码'
    supplier_choice = 1 #默认的网络提供商为联通，如果主要连接至其他网络提供商，将1更改为0-4的其他数值
    bg = BUPTGateway()
    #设置用户信息，并接受返回的post数据
    post_data = bg.set_user_info(userid, passwd, supplier_choice)
    network_status = bg.check_network()
    if network_status:
        bg.login(login_addr, post_data)
    else:
        print("网络连接错误，请检查网络")