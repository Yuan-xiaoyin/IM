# -*- encoding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import setting as st
import socket
import re

# 注册类
class Register():
	def __init__(self, parent_widget):
		# 创建注册窗口
		self.reg_widget = tk.Toplevel(parent_widget)
		self.reg_widget.title('用户注册')
		self.reg_widget.resizable(0, 0)

		# 设置窗口尺寸及位置
		w_width = 750
		w_height = 500
		screen_width = self.reg_widget.winfo_screenwidth()
		screen_height = self.reg_widget.winfo_screenheight()
		w_x = (screen_width - w_width) // 2
		w_y = (screen_height - w_height) // 2
		self.reg_widget.geometry('%dx%d+%d+%d' % (w_width, w_height, w_x, w_y))
		# 绑定回车事件
		self.reg_widget.bind('<Return>', func=self.call_register)

		# 创建控件
		self.name = tk.Label(self.reg_widget, text='用户名', width=6)
		self.nickname = tk.Label(self.reg_widget, text='昵称', width=6)
		self.passwd = tk.Label(self.reg_widget, text='密码', width=6)
		self.re_passwd = tk.Label(self.reg_widget, text='重复密码', width=6)
		self.name_input = tk.Entry(self.reg_widget, validate='focusout',
								   validatecommand=self.check_name, invalidcommand=self.name_error)
		self.nick_input = tk.Entry(self.reg_widget, validate='focusout',
								   validatecommand=self.check_nick, invalidcommand=self.nick_null)
		self.ntips = tk.StringVar()
		self.ntips.set('')
		self.nick_tips = tk.Label(self.reg_widget, textvariable=self.ntips, font='微软雅黑 10', fg='red')
		self.name_tips = tk.Label(self.reg_widget, font='微软雅黑 10', text='请输入6-16位用户名,可以使用字母,数字,下划线;只能以字母开头,不区分大小写')
		self.passwd_input = tk.Entry(self.reg_widget, show='*', validate='focusout',
								   validatecommand=self.check_pwd, invalidcommand=self.pwd_error)
		self.passwd_tips = tk.Label(self.reg_widget, font='微软雅黑 10', text='请输入8-20位密码,不能包含空格等空字符')
		self.repasswd_input = tk.Entry(self.reg_widget, show='*', validate='focusout',
									   validatecommand=self.check_rpwd, invalidcommand=self.rpwd_error)
		self.tips = tk.StringVar()
		self.tips.set('')
		self.rpwd_tips = tk.Label(self.reg_widget, font='微软雅黑 10', textvariable=self.tips, fg='red')
		self.btn_register = tk.Button(self.reg_widget, text='注册', width=20, height=2, font='微软雅黑 16 bold', command=self.register)
		
		# 放置控件
		self.name.place(x=190, y=40)
		self.nickname.place(x=190, y=100)
		self.passwd.place(x=190, y=160)
		self.re_passwd.place(x=190, y=220)

		self.name_input.place(x=270, y=40)
		self.nick_input.place(x=270, y=100)
		self.passwd_input.place(x=270, y=160)
		self.repasswd_input.place(x=270, y=220)

		self.name_tips.place(x=270, y=70)
		self.nick_tips.place(x=270, y=130)
		self.passwd_tips.place(x=270, y=190)
		self.rpwd_tips.place(x=270, y=250)
		self.btn_register.place(x=270, y=300)


	# 检查用户名合法性
	def check_name(self):
		name = self.name_input.get()
		replex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{5,15}$")
		if replex.findall(name):
			# print('账号输入合法')
			self.name_tips.configure(fg='black')
			return True
		else:
			# print('账号输入不合法')
			return False
	# 处理用户名不合法的情况
	def name_error(self):
		self.name_tips.configure(fg='red')

	# 检查昵称是否为空
	def check_nick(self):
		nick = self.nick_input.get()
		if not nick or len(nick) > 24:
			# self.ntips.set('请输入昵称')
			return False
		else:
			self.ntips.set('')
			return True
	# 提醒用户输入昵称
	def nick_null(self):
		self.ntips.set('请输入昵称,不超过24个字符')

	# 检查密码合法性
	def check_pwd(self):
		pwd = self.passwd_input.get()
		replex = re.compile(r"^\S{8,20}$")
		# print(replex)
		if replex.findall(pwd):
			# print('密码输入合法')
			self.passwd_tips.configure(fg='black')
			return True
		else:
			# print('密码输入不合法')
			return False
	# 提醒用户密码输入不合法
	def pwd_error(self):
		self.passwd_tips.configure(fg='red')

	# 检查两次密码输入是否一致
	def check_rpwd(self):
		pwd = self.passwd_input.get()
		rpwd = self.repasswd_input.get()
		if rpwd != pwd:
				# print('密码输入不合法')
			return False
		else:
			# print('密码输入合法')
			self.tips.set('')
			return True
	# 提醒用户两次密码不一致
	def rpwd_error(self):
		self.tips.set('两次密码输入不一致')

	# 回车事件通过此方法间接调用register函数
	def call_register(self, event):
		self.register()

	# 提交注册
	def register(self):
		name = self.name_input.get()
		nick = self.nick_input.get()
		pwd = self.passwd_input.get()
		rpwd = self.repasswd_input.get()

		# 合法性检查
		if not self.check_name():
			self.name_error()
			return
		if not self.check_nick():
			self.nick_null()
			return
		if not self.check_pwd():
			self.pwd_error()
			return
		if not self.check_rpwd():
			self.rpwd_error()
			return

		# 向服务器发起注册请求
		sockfd = socket.socket()
		try:
			sockfd.connect(st.ADDR)
			sockfd.send(('RGS' + name + ' ' + pwd + ' ' + nick).encode())
			result = sockfd.recv(1024).decode()
		except:
			tk.messagebox.showerror(title='注册失败', message='无法连接到服务器，请检查网络！')
			sockfd.close()
			return
		if result[:2] == 'OK':
			answer = tk.messagebox.askyesno(title='注册成功', message='注册成功！现在登录？')
			# print(answer)
			if answer == True:
				self.reg_widget.destroy()
		else:
			tk.messagebox.showwarning(title='注册失败', message=result)

		sockfd.close()




if __name__ == '__main__':
	reg = Register()