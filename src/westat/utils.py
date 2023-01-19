import socket
import getpass

user_name = getpass.getuser() # 获取当前用户名
host_name = socket.gethostname() # 获取当前主机名
host_ip = socket.gethostbyname(socket.gethostname()) # 获取当前IP