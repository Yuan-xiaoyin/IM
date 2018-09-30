#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
    name: 胡中伟、尹元章
    e-mail: 83512272@qq.com，m18382426610_1@163.com
    time: 2018-07-31
    功能: 即时通软件客户端
'''

from socket import *
import login
import home



def run_client():
    '''
    客户端入口函数
    用于启动客户端并处理客户端主事件流程
    '''
    # 登录
    login_obj = login.Login()
    uid = login_obj.login()
    # 根据登录返回结果判断登录是否成功
    if uid:
        # print('用户', uid, '登录成功')
        # 登录成功，进入主界面
        home_page = home.HomePage(uid)


if __name__ == '__main__':
    run_client()