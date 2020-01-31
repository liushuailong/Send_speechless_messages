"""
本模块实现通讯类功能的封装；
1. 局域网内广播功能函数；
2. 局域网内使用UDP发送功能；
3. 获得本机IP；
"""
import socket
from mmcq_settings import *


def LAN_broadcasting(data):
    """
    LAN broadcasting 局域网广播
    """
    bcast_addr = ("255.255.255.255", 44444)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    udp_socket.sendto(data.encode("utf-8"), bcast_addr)
    udp_socket.close()


def UDP_send_data(ip, data):
    """
    局域网内使用UDP发送功能；
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(data.encode(ENCODING), (ip, 44444))
    udp_socket.close()


def get_ip():
    """
    获得本机的IP地址；
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except OSError as oe:
        print("请连接局域网！")
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip
