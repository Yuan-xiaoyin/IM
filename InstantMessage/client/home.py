# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
import socket
import setting
import add
import re
import threading
import time, datetime

class HomePage():
	def __init__(self, uid):
		self.uid = uid

		# 创建主界面窗口
		self.home_widget = tk.Tk()
		self.home_widget.title('即时通 (Instant Message)')
		self.home_widget.resizable(0,0)
		# self.home_widget.iconbitmap('./img/logo.ico')

		# 设置窗口尺寸和位置
		w_width = 800
		w_height = 600
		screen_width = self.home_widget.winfo_screenwidth()
		screen_height = self.home_widget.winfo_screenheight()
		w_x = (screen_width - w_width) // 2
		w_y = (screen_height - w_height) // 2
		self.home_widget.geometry('%dx%d+%d+%d' % (w_width, w_height, w_x, w_y))

		# 创建窗口控件
		self.frame_left = tk.Frame(self.home_widget, width=250, height=600, bg='#E6E6E6')
		self.frame_right = tk.Frame(self.home_widget, width=550, height=600, bg='#F5F5F5')
		self.directory = ttk.Treeview(self.frame_left, show='tree', height='30', padding=[10,0,0,0])
		self.directory.column('#0', width='238')
		self.msg_input = tk.Text(self.frame_right, width='77', height='5')
		self.msg_hist = tk.scrolledtext.ScrolledText(self.frame_right, width='77', height='28', state='disabled')
		self.btn_send = tk.Button(self.frame_right, text='发送', command=self.send_message)
		self.btn_hist = tk.Button(self.frame_right, text='消息记录', command=self.get_hist)
		self.btn_add = tk.Button(self.frame_left, text='添加好友', width='10', height='2', command=self.add_friend)
		self.title_text = tk.StringVar()
		self.title_text.set('')
		self.title_bar = tk.Label(self.frame_right, height='1', textvariable=self.title_text, bg='#F5F5F5')


		# 布置组件
		self.frame_left.place(x=0, y=0)
		self.frame_right.place(x=250, y=0)
		self.directory.place(x=0, y=0)
		self.btn_add.place(x=80, y=550)
		

		# 数据初始化
		self.directory.insert('', 0, 'friends', text='好友列表', values='friends')
		self.directory.insert('', 1, 'groups', text='在线聊天室', values='groups')
		self.show_friends()
		
		# 绑定事件
		self.directory.bind('<<TreeviewSelect>>', func=self.init_chat_widget)
		self.msg_input.bind('<Return>', func=self.call_send_message)


		# 新建线程用于接收消息
		self.recv_msg_thread = threading.Thread(target=self.recv_msg, args=())
		self.recv_msg_thread.setDaemon(True)
		self.recv_msg_thread.start()

		# 进入消息循环
		self.home_widget.mainloop()

	# 接收消息函数
	def recv_msg(self):
		connfd = socket.socket()
		try:
			connfd.connect(setting.ADDR)
			connfd.send(('RCV' + self.uid).encode())
			result = connfd.recv(1024).decode()
			if result == 'OK':
				while True:
					data = connfd.recv(4096).decode()
					msg_type = data[0] # 消息类型（群聊/私聊）
					data = data[1:]
					fid = data.split()[0] # 发送者ID
					fnick = ' '.join(data.split()[2:])[:int(data.split()[1])] # 发送者昵称
					msg = ' '.join(data.split()[2:])[int(data.split()[1]):] #消息内容
					# print(msg_type)
					# print(fid)
					# print(msg)
					# 以下为接收到的消息进行显示
					if msg_type == 'S':
						# 私聊消息
						self.directory.see(fid)
						self.directory.selection_set((fid,))
					elif msg_type == 'G':
						# 群消息
						self.directory.see('groups')
						self.directory.selection_set('groups')
					# 选择项获取焦点时窗口初始化自动调用get_hist()获取消息记录，故以下代码仅在消息记录功能实现之前临时使用
					# self.msg_hist['state'] = 'normal'
					# self.msg_hist.tag_config('recvMsg', foreground='orange', justify='left')
					# self.msg_hist.insert(tk.END, '%s(ID:%s) %s\n' % (fnick, fid, time.strftime('%Y-%m-%d %X', time.localtime())), 'recvMsg')
					# self.msg_hist.insert(tk.END, msg + '\n', 'recvMsg')
					# self.msg_hist.see(tk.END)
					# self.msg_hist['state'] = 'disabled'
			else:
				messagebox(title='错误', message='该用户已登录')
		except Exception as e:
			print(e)
			messagebox.showerror(title='连接错误', message='连接服务器失败')
		connfd.close()

	# 加载好友列表
	def show_friends(self):
		sockfd = socket.socket()
		try:
			sockfd.connect(setting.ADDR)
			sockfd.send(('FLS' + self.uid).encode())
			f_list = sockfd.recv(10240).decode()
			if f_list == 'NOT_FOUND':
				sockfd.close()
				return
			f_list = f_list.split('<|?|.|<')
			# print(f_list)
			for item in f_list:
				if item:
					iid = re.findall(r'\d+\)$', item)[0][:-1]
					regex = '\(ID: %s\)$' % iid
					str_id = re.findall(regex, item)[0]
					nick = item[:-len(str_id)]
					# print(iid, nick)
					self.directory.insert(parent='friends', index=tk.END, iid=iid, text=item, values=nick)
		except Exception as e:
			print(e)
			messagebox.showerror(title='连接失败', message='连接服务器失败，请检查网络！')
		sockfd.close()

	# 添加好友
	def add_friend(self):
		print('开始添加好友')
		add.AddFriend(self.uid, self.directory)
		print('添加好友完成')

	# 聊天窗口初始化
	def init_chat_widget(self, event):
		iid = self.directory.selection()[0]
		# print(iid)
		if self.directory.parent(iid) == 'friends' or iid == 'groups':
			
			if type(self.directory.item(iid)['values']) is list:
				nick = self.directory.item(iid)['values'][0]
			else:
				nick = self.directory.item(iid)['values']
			# print('开始私聊:', 'FID:', iid, 'nick:', nick)
			if iid == 'groups':
				self.title_text.set('在线聊天室')
			else:
				self.title_text.set('%s(%s)' % (nick, iid))

			# 初始化聊天记录
			self.msg_hist['state'] = 'normal'
			self.msg_hist.delete('0.0', tk.END)
			self.msg_hist['state'] = 'disabled'
			self.get_hist(True)

			# 布置聊天窗口控件
			self.msg_input.place(x=0, y=480)
			self.msg_hist.place(x=0, y=22)
			self.btn_send.place(x=500, y=570)
			self.btn_hist.place(x=480, y=455)
			self.title_bar.place(x=10, y=0)
		else:
			# 隐藏聊天窗口控件
			self.msg_input.place_forget()
			self.msg_hist.place_forget()
			self.btn_send.place_forget()
			self.btn_hist.place_forget()
			self.title_bar.place_forget()



	# 发送消息
	def send_message(self):
		fid = self.directory.selection()[0]
		msg = self.msg_input.get('0.0', tk.END).rstrip()
		if msg == '':
			return
		# print(fid)
		# print(msg)
		if fid == 'groups':  # 群聊
			data = ('GRP' + self.uid + ' ' + fid + ' ' + msg).encode()
		else:	# 私聊
			data = ('SND' + self.uid + ' ' + fid + ' ' + msg).encode()

		connfd = socket.socket()
		try:
			connfd.connect(setting.ADDR)
			connfd.send(data)
			result = connfd.recv(1024).decode()       # 从服务端获取消息发送结果
			# print(result)
			if result[:2] == 'OK':
				# 在消息窗口中显示消息
				self.msg_hist['state'] = 'normal'
				self.msg_hist.tag_config('sendMsg', foreground='blue', justify='right')
				self.msg_hist.insert(tk.END, '%s(ID:%s) %s\n' % (result[2:], self.uid, time.strftime('%Y-%m-%d %X', time.localtime())), 'sendMsg')
				self.msg_hist.insert(tk.END, msg+'\n', 'sendMsg')
				self.msg_hist.see(tk.END)
				self.msg_input.delete('0.0', tk.END)
				self.msg_hist['state'] = 'disabled'
			else:
				# 好友不在线，发送失败
				tk.messagebox.showerror(title='发送失败', message=result)
				self.msg_input.delete('0.0', tk.END)
		except Exception as e:
			print(e)
			tk.messagebox.showerror(title='发送失败', message='连接服务器出错')
		
		connfd.close()


	# 事件调用发送消息函数
	def call_send_message(self, event):
		self.send_message()


	# 获取消息记录
	def get_hist(self, init=False):
		fid = self.directory.selection()[0]
		if fid == 'groups':	# 群聊
			fid = '9999'
		connfd = socket.socket()
		if init == False:	# 用户点击消息记录按钮触发
			request = 'HISF' + self.uid + ' ' + fid
		else:				# 聊天窗口初始化时触发
			request = 'HIST' + self.uid + ' ' + fid
		try:
			connfd.connect(setting.ADDR)
			connfd.send(request.encode())
			result = connfd.recv(40960).decode()
			data = result[3:]
			msg_list = data.split('<|?|.|<')
			# 没有符合条件的消息记录
			if result == 'NFD':
				if init:	# 页面初始化时触发
					return
				tk.messagebox.showerror(title='查询结果', message='没有相关记录')
				connfd.close()
				return
			# 服务端查询时出现异常
			if not msg_list:
				tk.messagebox.showerror(title='查询失败', message=result)
				connfd.close()
				return

			self.msg_hist['state'] = 'normal'
			self.msg_hist.delete('0.0', tk.END)
			self.msg_hist['state'] = 'disabled'

			# 按格式显示消息记录
			for msg in msg_list:
				# print(msg)
				uid = re.findall(r'\(ID:\d{5,10}\) ', msg)[0][4:-2]
				if uid == self.uid:
					self.msg_hist['state'] = 'normal'
					self.msg_hist.tag_config('sendMsg', foreground='blue', justify='right')
					self.msg_hist.insert(tk.END, msg, 'sendMsg')
					self.msg_hist.see(tk.END)
					self.msg_hist['state'] = 'disabled'
				else:
					self.msg_hist['state'] = 'normal'
					self.msg_hist.tag_config('recvMsg', foreground='orange', justify='left')
					self.msg_hist.insert(tk.END, msg, 'recvMsg')
					self.msg_hist.see(tk.END)
					self.msg_hist['state'] = 'disabled'
		except Exception as e:
			print(e)
			tk.messagebox.showerror(title='查询失败', message='连接服务器失败，请稍后重试')
		connfd.close()


if __name__ == '__main__':
	hp = HomePage('10003')