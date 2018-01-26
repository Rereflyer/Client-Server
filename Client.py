#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

# ip_address = '10.78.115.47'
ip_address = '127.0.0.1'

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 建立连接:
	s.connect((ip_address, 9999))

	# 接收欢迎消息:
	print s.recv(1024)

	# 发送数据:
	s.send('name19')
	s.close()
