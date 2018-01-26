#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import time

# ip_address = '10.78.115.47'
ip_address = '127.0.0.1'

name_ip_dict = {}


def tcplink(sock, address):
	global name_ip_dict
	name_ip_list = []

	print 'Accept new connection from %s:%s...' % address
	sock.send('Welcome!')

	while True:
		data = sock.recv(1024)
		time.sleep(1)
		if data == 'exit' or not data:
			break

		with open('clients.txt', 'r+') as f:
			try:
				name_ip_list = f.readlines()
			except IOError as e:
				print "read file error: " + str(e)

			if len(name_ip_list) != 0:
				for name_ip in name_ip_list:
					name_ip = name_ip.strip('\n')
					if len(name_ip.split(':')) == 2:
						(client_name, client_ip) = name_ip.split(':')
						name_ip_dict.setdefault(client_name, client_ip)
					else:
						print "clients.txt is error"

			if data in name_ip_dict.keys():
				if not address[0] in name_ip_dict.values():
					f.seek(0)                   # 将文件指针移动到文件起始
					file_str = f.read()
					file_str = file_str.replace(name_ip_dict[data], address[0])    # 将既有IP地址替换为新的IP地址
					try:
						f.seek(0)               # 将文件指针移动到文件起始
						f.write(file_str)
						f.close()               # 关闭当前文件
					except IOError as e:
						print "write file error: " + str(e)
				else:
					f.close()                       # 关闭当前文件
			else:
				try:
					# 直接将设备名+IP地址写入文件下一行
					if len(name_ip_dict) != 0:
						f.write('\n')
					f.writelines(data + ':' + address[0])
					f.close()                       # 关闭当前文件
				except IOError as e:
					print "write file error: " + str(e)

			name_ip_dict.clear()            # 清空字典，便于下一次使用
			break

	sock.close()
	print 'Connection from %s:%s closed.' % address


if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind ip address and port
	s.bind((ip_address, 9999))

	# 5 means max connect client
	s.listen(5)
	print 'Waiting for connection...'

	while True:
		# 接受一个新连接:
		sock, addr = s.accept()
		# 创建新线程来处理TCP连接:
		t = threading.Thread(target=tcplink, args=(sock, addr))
		t.start()
