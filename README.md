# Send_speechless_messages
使用python3.6，wxpython开发的局域网聊天软件，模仿“飞鸽传书”。  
英文名称：   Send_speechless_messages
## 版本信息

### v0.1

v0.1版本实现了局域网聊天的基本功能： 
 
- 程序主窗口的搭建；  
- 聊天程序窗口的搭建；  
- 程序启动时创建自己的名片在局域网内广播自己的名片，将自己的名片放到名片夹里；  
- 程序监听端口的数据流，对收到的不同数据进行处理；      
    - 当数据是以字符串“usr_card#"开头的话，对方发送的数据是对方发送的名片信息，
      信息的格式是”usr_card#id#usr_name#host_name"，根据名片信息建立名片，
      将名片放入名片夹内，同时将自己的名片回发给对方；  
    - 当数据是以字符串”message#“开头的话，对方发送的数据是聊天的信息，
      信息的格式为“message#send_id#accept_ip#Msg", 根据信息里面send_ip的标识，
      将信息显示在以该send_ip最为唯一标识的聊天窗口里面，
      [以下为还没有实现该功能,现阶段只有打开的好友才会显示到窗口，若没有则丢弃信息]
      若没有该聊天窗口则保存信息并告诉用户该send标识的好友发来了信息，请及时查收。
- [没有实现]用户主界面下面部分的设计；

- [没有实现]当用户列表里面需要呈现的面板大小超出实际面板大小时，形成带有滚动条的界面；
- [没有实现]当关闭程序主窗口时程序完全退出，现阶段程序还在后端运行，只是界面关闭；
    1. 关闭监听端口，并发送广播本机关闭的信息；
    2. 
- [没有实现]文件传输；
- [没有实现]配置信息的加载，更新，和保存；
- [没有实现]用户头像图标的获取并显示，现阶段是使用的统一的图标；
- [没有实现]用户状态控件的美化，用户状态的改变应该和具体的事件向关联，现阶段无作用；
- [没有实现]在代码包里面完善作者，版本等；
        
## 项目目录树

- mmcq_manage.py
项目启动的入口： python mmcq_manage.py 
- mmcq_GUI.py
	- class UsrSheetShow  
	使用设备上下文和计时器动态的将用户列表刷新绘制到用户列表，但实现起来困难，也没有达到目的；该类已弃用。
	- class UsrsPanel()
	创建用户列表的panel；
    显示的用户列表实时刷新；
    - class GroupPanel()
    创建用户组列表的Panel
    - class MainFrame()
    程序的主窗口，运行程序后程序展示的画面；
    - class ChatFrame()
    聊天窗口，和特定用户聊天时弹出的窗口；需要将弹出窗口的用户id(本机id，方id）传过来并使用对方ID使用最为唯一标识这个窗口。
    - def main()
    启动程序app窗口的主函数
- mmcq_usersheet.py  
    用于建立局域网用户列表的建立；
    1. 当程序启动时，主动使用UDP协议向255.255.255.255端口发送广播包，默认端口为44444，广播包内容包括：用户名，主机名，IP，工作组；已启动飞鸽的用户通过2425端口收到此广播包后，就会在自己的用户列表中添加这个用户的用户名、工作组等信息，同时向对方IP发送本机用户的个人信息；
    2. 何监控44444端口的数据流，实时刷新局域网用户列表和聊天信息；解决方案问题4，
    3. 用户离线时发送一个离线广播包到255.255.255.255，收到此广播包的用户，根据包中的IP地址（也可能是多种判断标志或者包含硬件标识，比如网卡地址等）删除对方的用户列表信息；
	- class UsrCard()  
	用户名片类
	- class Reader()  
	创建一个线程用来读取监听UDP端口44444的数据流，根据数据的不同类型来处理数据。
	- class Listener()  
	创建一个线程用来监听本机UDP端口44444的数据流，将得到的数据交给Reader类的实例取处理。
	- class UserSheet()  
	用来创建用户名片夹(llist)创建自己的名片和朋友的名片，并保存在名片夹中；
- mmcq_settings.py  
    用来提取、更新、保存用户配置
    1. 程序初始化时从setting.ini中提取配置赋值给响应的变量；
    2. 程序运行时用户更改配置,将配置先信息更新到配置文件中；
    3. 
- setting.ini
    配置数据保存的文件
- mmcq_socket.py
    - def LAN_broadcasting(data)  
        用于进行局域网广播
    - def UDP_send_data(ip, data)  
        用于使用UDP协议向IP指向的地址发送数据data;
    - def get_ip()  
        用于获得本机在局域网中的IP地址；

## 项目所使用的包及作用

### 虚拟环境的安装何使用

- virtualenv和conda虚拟环境的简介  

- virtualenv虚拟环境的使用  

    - 虚拟环境的创建  
    mkvirtualenv -p /usr/bin/python3 env_name
    - 虚拟环境的退出  
    deactivate
    - 虚拟环境的删除  
    rmvirtualenv env_name
    - 虚拟环境的切换  
    workon env_name

### 安装wxpython包

- 直接使用pip命令安装，但很多时候由于网络环境问题，需要时间长而且很多时候都会应为超时而导致安装失败；  
pip install wxpython
- 下载安装包：从pipy网站  
[PyPI_wxpython下载地址](https://pypi.org/project/wxPython/#files)
- 安装依赖包：  
sudo apt install make gcc libgtk-3-dev libwebkitgtk-dev libwebkitgtk-3.0-dev libgstreamer-gl1.0-0 freeglut3 freeglut3-dev python-gst-1.0 python3-gst-1.0 libglib2.0-dev ubuntu-restricted-extras libgstreamer-plugins-base1.0-dev
- 从解压包中安装wxpython  
python setup.py install

### 需要掌握的GUI工具包

- wx_python:GUI包  
    This website is all about wxPython, the cross-platform GUI toolkit for 
    the Python language. With wxPython software developers can create truly 
    native user interfaces for their Python applications, that run with 
    little or no modifications on Windows, Macs and Linux or other unix-like 
    systems.  
    [wxpython 视频教程](https://www.bilibili.com/video/av47145230?p=1)
- tkinter:GUI包
- pygame：用来写游戏也可用来写界面

### 网络和进程间通讯相关的包  

- socket：网络将通讯，分为UDP/TCP
- 


## 项目结构和功能 


