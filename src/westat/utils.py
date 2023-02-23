import socket
import getpass
import os

user_name = getpass.getuser() # 获取当前用户名
host_name = socket.gethostname() # 获取当前主机名
host_ip = socket.gethostbyname(socket.gethostname()) # 获取当前IP

current_path = os.path.dirname(os.path.abspath(__file__)) # 获取当前路径
