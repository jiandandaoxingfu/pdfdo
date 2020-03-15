# -*- coding: utf-8 -*-
# @Author:             old jia
# @Email:              jiaminxin@outlook.com
# @Date:               2019-06-26 19:39:18
# @Last Modified by:   old jia
# @Last Modified time: 2019-06-26 19:45:57

import http.server
import os

PORT = 8080

def callback(a, b, c):
	os.system('chrome localhost')
	print(1)

if __name__ == "__main__":
	try:
		server = http.server.HTTPServer(("", PORT), callback)
		print("HTTP server is starting at port "+repr(PORT)+'...')
		print("Press ^C to quit")
		server.serve_forever()
	except KeyboardInterrupt:
		print("^Shutting down server...")
		server.socket.close()
