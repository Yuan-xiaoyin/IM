# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import setting as st
import socket
import re
import register

# 登录类
class Login():
	def __init__(self):
		self.uid = None

		# 创建登录窗口
		self.login_widget = tk.Tk()
		self.login_widget.title("用户登录")
		self.login_widget.resizable(0,0)

		# 设置窗口尺寸和位置
		w_width = 600
		w_height = 400
		screen_width = self.login_widget.winfo_screenwidth()
		screen_height = self.login_widget.winfo_screenheight()
		w_x = (screen_width - w_width) // 2
		w_y = (screen_height - w_height) // 2
		self.login_widget.geometry('%dx%d+%d+%d' % (w_width, w_height, w_x, w_y))
		# 绑定回车事件
		self.login_widget.bind('<Return>', func=self.call_usr_login)

		# 创建窗口的控件
		self.usr_name = tk.Label(self.login_widget, text="账号")
		self.usr_pwd = tk.Label(self.login_widget, text="密码")
		self.name_tips = tk.StringVar()
		self.name_tips.set('')
		self.pwd_tips = tk.StringVar()
		self.pwd_tips.set('')
		self.name_input = tk.Entry(self.login_widget, validate='focusout', 
								  validatecommand=self.check_name, invalidcommand=self.name_error)
		self.pwd_input = tk.Entry(self.login_widget, show="*", validate='focusout',
								  validatecommand=self.check_pwd, invalidcommand=self.pwd_error)
		self.name_warning = tk.Label(self.login_widget, fg='red', textvariable=self.name_tips)
		self.pwd_warning = tk.Label(self.login_widget, fg='red', textvariable=self.pwd_tips)
		self.remember_pwd = tk.Checkbutton(self.login_widget, text="记住密码")
		self.btn_login = tk.Button(self.login_widget, text="登录", width=10, height=2, command=self.usr_login)
		self.btn_register = tk.Button(self.login_widget, text="注册", width=10, height=2, command=self.usr_register)
		self.version = tk.Label(self.login_widget, text='Ver 1.0.1', fg='#999', font='微软雅黑,10')
		self.author = tk.Label(self.login_widget, text='By  非常5+2', fg='#999', font='微软雅黑,10')

		# 布置控件
		self.usr_name.place(x=150, y=140)
		self.usr_pwd.place(x=150, y=200)
		self.name_input.place(x=200, y=140)
		self.pwd_input.place(x=200, y=200)
		self.name_warning.place(x=200, y=170)
		self.pwd_warning.place(x=200, y=230)
		self.remember_pwd.place(x=200, y=260)
		self.btn_login.place(x=150, y=310)
		self.btn_register.place(x=300, y=310)
		self.version.place(x=510, y=350)
		self.author.place(x=500, y=370)

	# 进入登录界面消息循环
	def login(self):
		self.login_widget.mainloop()
		# print('登录完成')
		return self.uid


	# 利用正则表达式检查用户名输入是否合法
	def check_name(self):
		name = self.name_input.get()
		replex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{5,15}$")
		if replex.findall(name):
			# print('账号输入合法')
			self.name_tips.set('')
			return True
		else:
			# print('账号输入不合法')
			return False

	# 用户名输入不合法
	def name_error(self):
		self.name_tips.set('请输入6-16位账号，包含字母、数字、下划线，只能以字母开头')

	# 利用正则表达式检查密码输入是否合法
	def check_pwd(self):
		pwd = self.pwd_input.get()
		replex = re.compile(r"^\S{8,20}$")
		if replex.findall(pwd):
			# print('密码输入合法')
			self.pwd_tips.set('')
			return True
		else:
			# print('密码输入不合法')
			return False

	# 密码输入不合法
	def pwd_error(self):
		self.pwd_tips.set('请输入8-20位密码，不能输入空格等')

	# 登录事件绑定
	def call_usr_login(self, event):
		self.usr_login()

	# 登录提交
	def usr_login(self):
		# print("Test of login...")
		# 进行用户名、密码合法性检查
		name = self.name_input.get()
		pwd = self.pwd_input.get()

		# 账号及密码合法性检查
		if not self.check_name():
			self.name_error()
			return
		if not self.check_pwd():
			self.pwd_error()
			return

		# 向服务器发起登录请求
		sockfd = socket.socket()
		try:
			sockfd.connect(st.ADDR)
			sockfd.send(('LGI' + name + ' ' + pwd).encode())
			result = sockfd.recv(1024).decode()
		except:
			tk.messagebox.showerror(title='登录失败', message='连接服务器失败')
			sockfd.close()
			return

		if result[:2] == 'OK':
			tk.messagebox.showinfo(title='登录成功', message='欢迎使用')
			self.uid = result[3:]
			self.login_widget.destroy()
		else:
			tk.messagebox.showwarning(title='登录失败', message=result)

		sockfd.close()

	# 转到注册页
	def usr_register(self):
		# print('开始注册')
		register.Register(self.login_widget)
		# print('注册页已关闭')



if __name__ == '__main__':
	login_obj = Login()