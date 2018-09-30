#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
    name: 胡中伟、尹元章
    e-mail: 83512272@qq.com,m18382426610_1@163.com
    time: 2018-07-31
    功能: 即时通软件服务端
'''

from socket import *
from threading import Thread
import setting as st
import sys
import pymysql

class ChatServer(object):
    """
    ChatServer类
    用于接收客户端连接并处理相关请求
    """

    # 类的初始化方法,用于创建tcp套接字对象并绑定服务器地址
    def __init__(self, addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.addr = addr

        # 用于保存在线用户列表
        self.online_dict = {}

        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(addr)
        self.sockfd.listen(10)
        
    # 启动服务器,循环监听客户端连接
    def run_server(self):
        while True:
            try:
                print("Waiting for connect...")
                connfd, addr = self.sockfd.accept()
                print('Connected from', addr)
            except Exception as e:
                print(e)
                continue
                
            new_client = Thread(target=self.client_handler, args = (connfd, addr))
            new_client.setDaemon(True)
            new_client.start()

    # 客户端连接到服务端后,新建线程调用此方法进行处理
    def client_handler(self, connfd, addr):
        while True:
            msg = connfd.recv(1024).decode()
            print(msg)
            if not msg:
                try:
                    self.online_dict.pop(uid)
                    print(uid, '退出登录')
                except:
                    pass
                connfd.close()
                print(addr, '客户端退出')
                sys.exit('客户端退出')
            # 有新客户端接收消息线程连接到服务器
            if msg[:3] == 'RCV':
                uid = msg[3:]
                # 判断用户是否已经登录
                if self.online_dict.get(uid, None) is None:
                    self.online_dict[uid] = connfd
                    connfd.send('OK'.encode())
                else:
                    connfd.send('该用户已登录'.encode())
            if msg[:3] == 'LGI':
                self.usr_login(connfd, addr, msg[3:])
            if msg[:3] == 'RGS':
                self.usr_register(connfd, msg[3:])
            if msg[:3] == 'ADD':
                self.add_friend(connfd, msg[3:])
            if msg[:3] == 'FLS':
                self.find_friends_list(connfd, msg[3:])
            if msg[:3] == 'SND' or msg[:3] == 'GRP':
                self.send_massage(connfd, msg[3:])
            if msg[:3] == 'HIS':
                self.get_hist(connfd, msg[3:])

    # 处理用户登录请求
    def usr_login(self, connfd, addr, request):
        name = request.split()[0]
        passwd = request.split()[1]

        # 连接数据库检查用户名及密码
        try:
            conn_db = pymysql.connect(host=st.DBHOST, port=st.DBPORT, db=st.DBNAME, charset=st.DBCHARSET, user=st.DBUSER, passwd=st.DBPASSWD)
        except:
            connfd.send(('连接数据库服务器失败！').encode())
            return
        cur = conn_db.cursor()
        cur.execute("select ID from user_info where name='%s' and passwd='%s';" % (name, passwd))
        uid = cur.fetchone()
        try:
            if uid:
                # 重复登录验证
                if self.online_dict.get(str(uid[0]), None) is not None:
                    connfd.send('该用户已登录，请不要重复登录！'.encode())
                    cur.close()
                    conn_db.close()
                    return
                cur.execute("update user_info set last_time=now() where ID=%s;" % str(uid[0]))
                connfd.send(('OK ' + str(uid[0])).encode())
            else:
                connfd.send('用户名或密码错误'.encode())
            conn_db.commit()
        except:
            conn_db.rollback()
            connfd.send('服务器错误！请稍后重试。'.encode())
        cur.close()
        conn_db.close()

    # 处理用户注册请求
    def usr_register(self, connfd, request):
        name = request.split()[0]
        passwd = request.split()[1]
        nick = ' '.join(request.split()[2:])

        # 连接数据库检查用户名是否存在
        try:
            conn_db = pymysql.connect(host=st.DBHOST, port=st.DBPORT, db=st.DBNAME, charset=st.DBCHARSET, user=st.DBUSER, passwd=st.DBPASSWD)
        except:
            connfd.send(('连接数据库服务器失败！').encode())
            return
        cur = conn_db.cursor()
        cur.execute("select * from user_info where name='%s';" % name)
        if not cur.fetchone():
            try:
                cur.execute("insert into user_info(name,passwd,nick_name, register_time) \
                            values('%s','%s','%s',now());" % (name, passwd, nick))
                conn_db.commit()
                connfd.send(('OK ' + '注册成功！').encode())
            except:
                conn_db.rollback();
                connfd.send(('注册失败！请稍后重试。').encode())
        else:
            connfd.send(('用户名已存在！请重新输入...').encode())
        cur.close()
        conn_db.close()

    # 处理客户端添加好友请求
    def add_friend(self, connfd, request):
        uid = request.split()[0]
        fid = ' '.join(request.split()[1:])
        # 连接数据库检查用户名是否存在
        try:
            conn_db = pymysql.connect(host=st.DBHOST, port=st.DBPORT, db=st.DBNAME, charset=st.DBCHARSET, user=st.DBUSER, passwd=st.DBPASSWD)
        except:
            connfd.send(('连接数据库服务器失败！').encode())
            return
        cur = conn_db.cursor()
        try:
            if fid.isdigit():
                # 用户查找的是ID号
                cur.execute("select * from user_info where ID=%s;" % fid)
                find_result = cur.fetchone()
                if not find_result:
                    connfd.send('未找到该用户，请确认用户是否存在！'.encode())
                    cur.close()
                    conn_db.close()
                    return
            else:
                # 用户查找的是用户名
                cur.execute("select * from user_info where name='%s';" % fid)
                find_result = cur.fetchone()
                # print('find_result: ', find_result)
                # print('find_result[0]: ', find_result[0], type(find_result[0]))
                if not find_result:
                    connfd.send('未找到该用户，请确认用户是否存在！'.encode())
                    cur.close()
                    conn_db.close()
                    return
                elif find_result[0] == int(uid):
                    connfd.send('不能添加自己！'.encode())
                    cur.close()
                    conn_db.close()
                    return
            # 查找到指定用户，操作数据库中好友关系表
            fid = find_result[0]
            nick_name = find_result[5]
            cur.execute("select * from friends where uid=%s and fid=%s;" % (uid, fid))
            fetch1 = cur.fetchone()
            cur.execute("select * from friends where uid=%s and fid=%s;" % (fid, uid))
            fetch2 = cur.fetchone()
            if fetch1 or fetch2:
                connfd.send('该用户已经是您的好友，请不要重复添加！'.encode())
                cur.close()
                conn_db.close()
                return
            cur.execute("insert into friends(uid,fid,add_time) values(%s,%s,now());" % (uid, fid))
            conn_db.commit()
            connfd.send(('OK' + nick_name + '(ID: ' + str(fid) + ')').encode())
        except Exception as e:
            print(e)
            conn_db.rollback()
            connfd.send('添加失败，请稍后重试！'.encode())
        cur.close()
        conn_db.close()

    # 处理客户端好友列表数据请求
    def find_friends_list(self, connfd, uid):
        f_list = ''
        result = tuple()
        try:
            conn_db = pymysql.connect(host=st.DBHOST, port=st.DBPORT, db=st.DBNAME, charset=st.DBCHARSET, user=st.DBUSER, passwd=st.DBPASSWD)
        except:
            connfd.send(('连接数据库服务器失败！').encode())
            return
        cur = conn_db.cursor()
        try:
            # 获取用户所有好友ID
            cur.execute("select fid from friends where uid=%s;" % uid)
            result += cur.fetchall()
            cur.execute("select uid from friends where fid=%s;" % uid)
            result += cur.fetchall()
            # print(result)
            # 逐个获取好友昵称
            for item in result:
                # print(item)
                f_id = item[0]
                # print(f_id)
                cur.execute("select nick_name from user_info where ID=%d;" % f_id)
                nick_name = cur.fetchone()[0]
                f_list += nick_name + '(ID: ' + str(f_id) + ')' + '<|?|.|<'         # 使用特殊字符<|?|.|<分隔，防止粘包
            if f_list:  # 该用户有好友
                connfd.send(f_list.encode())
            else:       # 该用户暂无好友
                connfd.send('NOT_FOUND'.encode())
        except Exception as e:
            print(e)
            connfd.send('好友初始化失败！'.encode())
        cur.close()
        conn_db.close()


    # 处理客户端发送消息请求
    def send_massage(self, connfd, request):
        uid = request.split()[0]
        fid = request.split()[1]
        msg = request[len(uid)+len(fid)+2:]
        # print(fid)
        # print(msg)
        if fid == 'groups':     # 群消息
            for usr in self.online_dict:
                if usr != uid:
                    try:
                        conn_db = pymysql.connect(host=st.DBHOST, port=st.DBPORT, db=st.DBNAME, charset=st.DBCHARSET, user=st.DBUSER, passwd=st.DBPASSWD)
                        cur = conn_db.cursor()
                        cur.execute("select nick_name from user_info where ID=%s;" % uid)
                        unick = cur.fetchone()[0]
                        cur.execute("insert into chat_history(UID,FID,msg,send_time) values(%s,%d,'%s',now());" % (uid, 9999, msg)) # 9999表示在线聊天室消息
                        conn_db.commit()
                        # cur.execute("select nick_name from user_info where ID=%s;" % fid)
                        # fnick = cur.fetchone()[0]
                    except:
                        conn_db.rollback()
                        connfd.send('连接到数据库失败'.encode())
                        return
                    self.online_dict[usr].send(('G' + uid + ' ' + str(len(unick)) + ' ' + unick + msg).encode())
                    connfd.send(('OK' + unick).encode())
                    cur.close()
                    conn_db.close()
        else:   # 私聊消息
            if self.online_dict.get(fid, None) is None:
                connfd.send('对方不在线'.encode())
                return
            else:
                try:
                    conn_db = pymysql.connect(host=st.DBHOST, port=st.DBPORT, db=st.DBNAME, charset=st.DBCHARSET, user=st.DBUSER, passwd=st.DBPASSWD)
                    cur = conn_db.cursor()
                    cur.execute("select nick_name from user_info where ID=%s;" % uid)
                    unick = cur.fetchone()[0]
                    cur.execute("insert into chat_history(UID,FID,msg,send_time) values(%s,%s,'%s',now());" % (uid, fid, msg))
                    conn_db.commit()
                    # cur.execute("select nick_name from user_info where ID=%s;" % fid)
                    # fnick = cur.fetchone()[0]
                except:
                    conn_db.rollback()
                    connfd.send('连接到数据库失败'.encode())
                    return
                self.online_dict[fid].send(('S' + uid + ' ' + str(len(unick)) + ' ' + unick + msg).encode())
                connfd.send(('OK' + unick).encode())
                conn_db.close()


    # 处理客户端获取消息记录请求
    def get_hist(self, connfd, request):
        isinit = request[0]
        uid = request[1:].split()[0]
        fid = request[1:].split()[1]
        try:
            conn_db = pymysql.connect(host=st.DBHOST, port=st.DBPORT, db=st.DBNAME, charset=st.DBCHARSET, user=st.DBUSER, passwd=st.DBPASSWD)
            cur = conn_db.cursor()
            if isinit == 'T':
                cur.execute("select last_time from user_info where ID=%s;" % uid)
                start_time = "\'" + str(cur.fetchone()[0]) + "\'"
            else:
                start_time = 'now() - interval 30 day'
            if fid == '9999':
                cur.execute("select UID,FID,msg,send_time from chat_history where FID=%s and send_time>%s;" % (fid, start_time))
            else:
                cur.execute("select UID,FID,msg,send_time from chat_history where ((UID=%s and FID=%s) or (FID=%s and UID=%s)) and send_time>%s;" % 
                            (uid, fid, uid, fid, start_time))
            result = cur.fetchall()
            # print(result)
            cur.execute("select nick_name from user_info where ID=%s;" % uid)
            unick = cur.fetchone()[0]
            if fid != '9999':
                cur.execute("select nick_name from user_info where ID=%s;" % fid)
                fnick = cur.fetchone()[0]

            msg = 'NFD'
            for m in result:
                if fid == '9999':
                    cur.execute("select nick_name from user_info where ID=%s;" % m[0])
                    unick = cur.fetchone()[0]
                    msg += '%s(ID:%s) %s\n%s\n<|?|.|<' % (unick, m[0], m[-1].strftime('%Y-%m-%d %X'), m[-2])
                else:
                    if str(m[0]) == uid:
                        msg += '%s(ID:%s) %s\n%s\n<|?|.|<' % (unick, uid, m[-1].strftime('%Y-%m-%d %X'), m[-2])
                    elif str(m[0]) == fid:
                        msg += '%s(ID:%s) %s\n%s\n<|?|.|<' % (fnick, fid, m[-1].strftime('%Y-%m-%d %X'), m[-2])
            if msg != 'NFD':
                msg = msg[:-7]
            # print(msg)
            connfd.send(msg.encode())
        except Exception as e:
            print(e)
            connfd.send(('查询出错：'+str(e)).encode())
        cur.close()
        conn_db.close()


if __name__ == '__main__':
    # 创建ChatServer类的示例对象
    chat_obj = ChatServer(st.ADDR)
    # 启动服务器
    chat_obj.run_server()
