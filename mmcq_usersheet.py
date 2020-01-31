"""
用于建立局域网用户列表的建立；
1. 当程序启动时，主动使用UDP协议向255.255.255.255端口发送广播包，默认端口为44444，
    广播包内容包括：用户名，主机名，IP，工作组；已启动飞鸽的用户通过2425端口收到此广播包后，
    就会在自己的用户列表中添加这个用户的用户名、工作组等信息，同时向对方IP发送本机用户的个人信息；
2. 如何监控44444端口的数据流，实时刷新局域网用户列表和聊天信息；解决方案问题4，
3. 用户离线时发送一个离线广播包到255.255.255.255，收到此广播包的用户，根据包中的IP地址（也可能
    是多种判断标志或者包含硬件标识，比如网卡地址等）删除对方的用户列表信息；

问题1：如何使用UDP协议向255.255.255.255：44444发送广播包；
    # 1、创建udp套接字
	# socket.AF_INET  表示IPv4协议  AF_INET6 表示IPv6协议
	# socket.SOCK_DGRAM  数据报套接字，只要用于udp协议
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# 2、准备接收方的地址
	# 元组类型  ip是字符串类型   端口号是整型
	dest_addr = ('10.10.10.10', 0000)
	# 要发送的数据
	send_data = "我是要发送的数据"
	# 3、发送数据
	udp_socket.sendto(send_data.encode("utf-8"), dest_addr)
	# 4、等待接收方发送的数据  如果没有收到数据则会阻塞等待，直到收到数据
	# 接收到的数据是一个元组   (接收到的数据, 发送方的ip和端口)
	# 1024  表示本次接收的最大字节数
	recv_data, addr = udp_socket.recvfrom(1024)
	# 5、关闭套接字
	udp_socket.close()
	###############################################

    import socket


    if __name__ == '__main__':
        # 创建socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 设置socket选项
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        # 发送广播消息
        udp_socket.sendto("hello".encode("gbk"), ("255.255.255.255", 8989))
        udp_socket.close()


问题2：广播包的内容机器解析；

问题3：如何得到主机的IP和主机名称（done）
    方法1    这样可以获取到本机所有网卡的IP地址：IPs = socket.gethostbyname_ex(socket.gethostname())[-1]
            如果想获取正在上网所使用的本机IP，通过route命令可以得到：
            Windows下用 [a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2]
            Linux下用 [a for a in os.popen('/sbin/route').readlines() if 'default' in a][0].split()[1]
    方法2
        import socket

        def get_host_ip():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            finally:
                s.close()

            return ip

问题4. 如何监控44444端口的数据流，实时刷新局域网用户列表和聊天信息；（done）
    “”“
    1. 监听TCP端口信息；
    2. 监听UDP端口信息；
    ”“”
    import threading
    import socket


    encoding = 'utf-8'
    BUFSIZE = 1024


    # a read thread, read data from remote
    class Reader(threading.Thread):
        def __init__(self, client):
            threading.Thread.__init__(self)
            self.client = client

        def run(self):
            while True:
                data = self.client.recv(BUFSIZE)
                if(data):
                    string = bytes.decode(data, encoding)
                    print(string, end='')
                else:
                    break
            print("close:", self.client.getpeername())

        def readline(self):
            rec = self.inputs.readline()
            if rec:
                string = bytes.decode(rec, encoding)
                if len(string)>2:
                    string = string[0:-2]
                else:
                    string = ' '
            else:
                string = False
            return string


    # a listen thread, listen remote connect
    # when a remote machine request to connect, it will create a read thread to handle
    class Listener(threading.Thread):
        def __init__(self, port):
            threading.Thread.__init__(self)
            self.port = port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", port))
            self.sock.listen(0)
        def run(self):
            print("listener started")
            while True:
                client, cltadd = self.sock.accept()
                Reader(client).start()
                cltadd = cltadd
                print("accept a connect")


    lst  = Listener(9011)   # create a listen thread
    lst.start() # then start

问题5. 如何设计存放用户信息的类（名片类）；
    usr_card#id#usr_name#host_name

"""

import socket
import threading
import time
from mmcq_settings import *
from mmcq_socket import *


class UsrCard(object):
    """
    用户名片类
    """

    def __init__(self, ip, host_name, usr_name,):
        self._ip = ip
        self._host_name = host_name
        self._usr_name = usr_name

    def __str__(self):
        return f"usr_card#{self._ip}#{self._host_name}#{self._usr_name}"

    def card_info(self):
        return f"usr_card#{self._ip}#{self._host_name}#{self._usr_name}"

    def ip(self):
        return self._ip

    def host_name(self):
        return self._host_name

    def usr_name(self):
        return self._usr_name


class Reader(threading.Thread):
    """
    读取监听UDP端口44444的数据流
    """
    def __init__(self, data, addr, main_frame):
        threading.Thread.__init__(self)
        self.data = data
        self.friend_ip = addr[0]
        print(self.friend_ip)
        # self.usr_sheet = usr_sheet
        self.main_frame = main_frame

    def run(self):

        if self.data:
            string_msg = bytes.decode(self.data, ENCODING)

            # 1. 将收到的信息进行分类，如果发送的是一个端口信息，则将该端口信息保存在名片中，
            if string_msg.startswith("usr_card#") and self.main_frame.usr_sheet.my_card.ip() != self.friend_ip:
                self.save_card(string_msg)
                # 当收到一个用户的卡片后我们要将我们的卡片回发给对方；
                # 同时将名片添加到名片夹中；
                self.send_my_card(string_msg.split("#")[1])
            # 2. 如果收到的信息是一个消息，则提醒用户并显示在响应的对话框中，并返回给发送方一个收到的消息；
            elif string_msg.startswith("message#") and self.main_frame.usr_sheet.my_card.ip() != self.friend_ip:
                self.main_frame.message_list.append(string_msg)
                for chat_frame_window in self.main_frame.pop_chat_window_list:
                    if chat_frame_window.friend_ip == self.friend_ip:
                        chat_frame_window.ShowMsg(string_msg)
            # 3. 当一个用户下线时向局域网内广播下线消息，其他用户将其从名片卡中删除；
            elif string_msg.startswith("exit#") and self.main_frame.usr_sheet.my_card.ip() != self.friend_ip:
                self.delete_card(string_msg)
                pass

    def delete_card(self, data):
        ip = data.split("#")[1]
        for usr_card in self.main_frame.usr_sheet.usr_sheet():
            if usr_card.ip() == ip:
                self.main_frame.usr_sheet.delete(usr_card)

    def save_card(self, string):
        usr_info = string.split("#")[1:]
        usr_card = UsrCard(*usr_info)
        self.main_frame.usr_sheet.add(usr_card)

    def send_my_card(self, friend_ip):
        my_card = self.main_frame.usr_sheet.my_card.card_info()
        UDP_send_data(friend_ip, my_card)


class Listener(threading.Thread):
    """
    监听UDP端口44444的数据流。

    """
    def __init__(self, main_frame, port=44444):
        threading.Thread.__init__(self)
        self.port = port
        self.main_frame = main_frame
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", port))
        # 将自己的地址广播到局域网中
        self.broadcast()

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            Reader(data, addr, self.main_frame).start()
            # print(f"read data:{data} from {addr}")

    def broadcast(self):
        data = self.main_frame.usr_sheet.my_card.card_info()
        LAN_broadcasting(data)


class UserSheet(object):

    def __init__(self):
        self.ip = self.get_ip()
        self.usr_name = self.get_usr_name()
        self.host_name = self.get_host_name()
        self.usersheet = []
        self.message_list = []
        self.my_card = UsrCard(self.ip, self.host_name, self.usr_name)
        self.start = 0

    def usr_sheet(self):
        return self.usersheet

    def add(self, usr_card):
        # 当收到用户的名片时将其添加到用户表单中
        self.usersheet.append(usr_card)

    def delete(self, usr_card):
        # 当用户收到朋友退出的消息时将朋友的名片从名片夹中删除
        self.usersheet.remove(usr_card)

    def remove(self, usr_card):
        # 当用户下线时从用户表单中移除用户名片
        self.usersheet.remove(usr_card)

    def __iter__(self):
        return self

    def __next__(self):
        # 迭代方法有问题，先不用。
        if self.start <= len(self.usersheet):
            self.start += 1
            return self.usersheet[self.start-1]
        else:
            raise StopIteration

    def get_ip(self):
        return get_ip()

    def get_usr_name(self):
        return socket.gethostname()

    def get_host_name(self):
        return socket.gethostname()

    def get_group_name(self):
        return "group_name"


if __name__ == '__main__':
    usr_sheet =UserSheet()
    Listener(usr_sheet).start()
    # UsrCard("ip","host","usr")
    while True:
        for i in usr_sheet.usersheet:
            print(i)

        time.sleep(60)
