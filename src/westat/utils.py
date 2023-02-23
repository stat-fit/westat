import socket
import getpass
import os

# 设备信息
user_name = getpass.getuser() # 获取当前用户名
host_name = socket.gethostname() # 获取当前主机名
host_ip = socket.gethostbyname(socket.gethostname()) # 获取当前IP

# 路径
current_path = os.path.dirname(os.path.abspath(__file__)) # 获取当前路径
