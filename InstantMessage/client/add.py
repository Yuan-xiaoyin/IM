import tkinter as tk
import socket
import setting
from tkinter import messagebox


class AddFriend():
	def __init__(self, uid, directory):
		self.uid = uid
		self.directory = directory

		# 创建添加好友窗口
		self.add_widget = tk.Tk()
		self.add_widget.title('添加好友')
		self.add_widget.resizable(0,0)
		# 设置窗口尺寸和位置
		w_width = 400
		w_height = 200
		screen_width = self.add_widget.winfo_screenwidth()
		screen_height = self.add_widget.winfo_screenheight()
		w_x = (screen_width - w_width) // 2
		w_y = (screen_height - w_height) // 2
		self.add_widget.geometry('%dx%d+%d+%d' % (w_width, w_height, w_x, w_y))
		# 绑定回车事件
		self.add_widget.bind('<Return>', func=self.call_find_friend)

		# 创建窗口控件
		add_label = tk.Label(self.add_widget, text='好友用户名或ID号')
		self.add_input = tk.Entry(self.add_widget)
		btn_add = tk.Button(self.add_widget, text='添加', command=self.find_friend, width='6', height='2')

		# 放置组件
		add_label.place(x=20, y=60)
		self.add_input.place(x=140, y=60)
		btn_add.place(x=180, y =120)

	# 与服务器交互，添加好友
	def find_friend(self):
		fid = self.add_input.get()
		if fid == self.uid:
			messagebox.showerror(title='添加失败', message='不能添加自己！')
			return
		sockfd = socket.socket()
		try:
			sockfd.connect(setting.ADDR)
			sockfd.send(('ADD' + self.uid + ' ' + fid).encode())
			result = sockfd.recv(1024).decode()
			if result[:2] == 'OK':
				messagebox.showinfo(title='添加成功', message='已成功添加好友(ID：%s)' % fid)
				self.directory.insert('friends', tk.END, text=result[2:])
				self.add_widget.destroy()

			else:
				messagebox.showerror(title='添加失败', message=result)
		except:
			messagebox.showerror(title='添加失败', message='连接服务器失败！')
		sockfd.close()

	# 回车事件函数
	def call_find_friend(self, event):
		self.find_friend()





if __name__ == '__main__':
	af = AddFriend('10001')