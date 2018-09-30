import pymysql
import setting

host = setting.HOST
user = 'root'
passwd = '0914'
charset = 'utf8'

conn = pymysql.connect(host=host, user=user, passwd=passwd, charset=charset)
cur = conn.cursor()

cur.execute("create database IM character set utf8 if not exist;")
cur.execute("use IM;")
cur.execute("create table user_info(\
			ID int primary key auto_increment,\
			name char(16),\
			passwd char(16) not null default '123456',\
			register_time datetime,\
			last_time datetime,\
			nick_name varchar(24),\
			logo varchar(128) not null default './image/user_logo.jpg',\
			status tinyint unsigned not null default 0)\
			auto_increment=10001, character set utf8;")


conn.commit()
cur.close()
conn.close()