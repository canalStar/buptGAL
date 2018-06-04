# 使用说明

    此目录为python3 版本的校园网网关登录、注销脚本
    login.py为登录脚本，使用格式为:
        python login.py [用户名] [密码]
        例如：
        python login.py 200101010101 password
        （你也可以更改login.py代码中的默认用户名及密码为你自己的用户名密码，以便不用每次都输入用户名密码）
        登录后会显示本地ip，连网时长，已用流量，账户余额等
    logout.py 为注销脚本，使用格式为：
        python logout.py
        无需输入参数
        注销时也会显示：联网时长，已用流量，账户余额等