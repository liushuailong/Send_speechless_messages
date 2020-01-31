"""
该模块负责‘眉目传情’项目GUI展示；
分为一下几个部分：
待定
"""

# import
from time import sleep

import wx
import os
from wx.lib.stattext import GenStaticText

# 导入本项目模块
from mmcq_settings import *
from mmcq_usersheet import *

CWD = os.getcwd()


class UsrSheetShow(wx.Window):
    """
    目的：使用设备上下文和计时器动态的将用户列表刷新的绘制到用户列表中。
    该类暂时没有达到目的；弃用
    """

    def __init__(self, usr_sheet, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.usr_sheet = usr_sheet
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)  # 绑定一个定时器事件
        self.timer.Start(1000)  # 设定时间间隔

    def Draw(self, dc):
        w, h = self.GetClientSize()
        str = "hello, word!"
        sw, wh = tw, th = dc.GetTextExtent(str)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.DrawText("hello,world", (w-sw)/2, (h-wh)/2)

    def showUI(self):
        """
        展示用户列表在界面的布局，在该类中如何使用，使用设备上下文将该函数内代码显示的内容，画到屏幕上；
        :return:
        """
        self.main_box = wx.BoxSizer(wx.VERTICAL)
        print("计时器开启计时")

        for usr_card in self.usr_sheet.usersheet:
            # 如何做到将用户列表里面的信息以垂直列表的形式添加到其中。
            head_sizer = wx.GridBagSizer(hgap=5, vgap=5)
            usr_photo = wx.Image("./images/profile_photo_v0.1.png", wx.BITMAP_TYPE_ANY)
            self.sbm_profile = wx.StaticBitmap(self, -1, wx.BitmapFromImage(usr_photo))
            self.sbm_profile.Bind(wx.EVT_LEFT_DCLICK, self.pop_chat_window)
            usr_name = usr_card.usr_name()
            host_name = usr_card.host_name()
            print(usr_name)
            self.usr_txt = GenStaticText(self, -1, label="用户名：")
            self.host_txt = GenStaticText(self, -1, label="主机名：")
            self.host_name = GenStaticText(self, -1, label=host_name)
            self.usr_name = GenStaticText(self, -1, label=usr_name)
            # 个人信息状态布局
            head_sizer.Add(self.sbm_profile, pos=(0, 0), span=(2, 1), flag=wx.EXPAND)
            head_sizer.Add(self.usr_txt, pos=(0, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
            head_sizer.Add(self.host_txt, pos=(1, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
            head_sizer.Add(self.usr_name, pos=(0, 2), flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
            head_sizer.Add(self.host_name, pos=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

            head_sizer.AddGrowableCol(2)
            self.main_box.Add(head_sizer, flag=wx.EXPAND | wx.ALL, border=5)

            self.SetSizerAndFit(self.main_box)

    def OnTimer(self, evt):  # 显示时间事件处理函数
        dc = wx.BufferedDC(wx.ClientDC(self))
        self.Draw(dc)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)


class UsrsPanel(wx.Panel):
    """
    创建用户列表的panel；
    显示的用户列表需要实时刷新；（没有实现）:思路使用wx.Timer类，定期事件。
    问题1：在wxpython中如何实时刷新一个面板上控件；
        想法1. 基础的，看看文档里有关wx.DC类的说明，稍微高级的试试wxpython里带的floatcanvas子模块。
        使用定时器和设备上下文实现该功能，类似代码为： 一个简单的数字时钟.py。
        方法一：直接用控件和布局来实现。用户列表示例
            失败： 当接收到新用户时无法接受，在屏幕上实时显示。
        方法二：使用wxpython计时器和设备上下文来动态刷新； 用户组列表1
            暂时还没有实现，复杂度高；且如何响应鼠标事件呢？
        方法三：列表控件；用户组列表
        方法四：使用定时器检查用户表单列表中的是否添加了新的用户，如果有一个新用户则添加一个新用户卡片。
            已实现 @@@@@@@@@@@@@@
    问题2：如何设定notebook标签下panal的大小；
        答案同问题5

    问题3：如何点击一片区域（用户显示区域）来弹出用户聊天对话框；
    问题4：用户信息和聊天信息如何正确传递到聊天对话框中；
        使用ip绑定到固定的窗口,通过消息里面的ip地址来找到对应的窗口,在将消息内容呈现在对应的窗口里。
    问题5：使用Sizer布局是如何，设置个控件个控件之间占据的距离；
        使用Sizer.Add()中的 proportion 比例选项来设置。
    问题6：如何将退出的用户从用户面板中删除。
        如何删除已有的控件；
    """
    def __init__(self, parent, main_frame):
        super(self.__class__, self).__init__(parent)
        self.usr_sheet = main_frame.usr_sheet
        self.main_frame = main_frame
        self.ip_list = []
        self.show_usr_sheet()
        # 设定定时器(不起作用）
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.Add_usr_card, self.timer)
        self.timer.Start(1000)

    def usr_card(self, usr_card):
        ip = usr_card.ip()
        head_sizer = wx.GridBagSizer(hgap=5, vgap=5)
        usr_photo = wx.Image("./images/profile_photo_v0.1.png", wx.BITMAP_TYPE_ANY)
        self.sbm_profile = wx.StaticBitmap(self, -1, wx.BitmapFromImage(usr_photo), name=ip)
        self.sbm_profile.Bind(wx.EVT_LEFT_DCLICK, self.pop_chat_window)
        usr_name = usr_card.usr_name()
        self.ip_list.append(ip)
        host_name = usr_card.host_name()
        self.usr_text = GenStaticText(self, -1, label="用户名：", name=ip)
        self.usr_text.Bind(wx.EVT_LEFT_DCLICK, self.pop_chat_window)
        self.host_text = GenStaticText(self, -1, label="IP地址：", name=ip)
        self.host_text.Bind(wx.EVT_LEFT_DCLICK, self.pop_chat_window)
        self.ip = GenStaticText(self, -1, label=ip, name=ip)
        self.ip.Bind(wx.EVT_LEFT_DCLICK, self.pop_chat_window)
        self.usr_name = GenStaticText(self, -1, label=usr_name, name=ip)
        self.usr_name.Bind(wx.EVT_LEFT_DCLICK, self.pop_chat_window)
        # 个人信息状态布局
        head_sizer.Add(self.sbm_profile, pos=(0, 0), span=(2, 1), flag=wx.EXPAND)
        head_sizer.Add(self.usr_text, pos=(0, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        head_sizer.Add(self.host_text, pos=(1, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        head_sizer.Add(self.usr_name, pos=(0, 2), flag=wx.EXPAND | wx.ALIGN_CENTER)
        head_sizer.Add(self.ip, pos=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

        head_sizer.AddGrowableCol(2)
        self.main_box.Add(head_sizer, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizerAndFit(self.main_box)

    def show_usr_sheet(self):
        """
        启动显示用户列表；
        :return: None
        """
        self.main_box = wx.BoxSizer(wx.VERTICAL)
        for usr_card in self.usr_sheet.usersheet:
            self.usr_card(usr_card)
            self.SetSizerAndFit(self.main_box)
        return None

    def Add_usr_card(self, event):
        for usr_card in self.usr_sheet.usersheet:
            if usr_card.ip() not in self.ip_list:
                self.usr_card(usr_card)

    def pop_chat_window(self, event):
        my_ip = self.usr_sheet.get_ip()
        friend_ip = wx.FindWindowById(event.GetId(), self).GetName()
        chat_frame = ChatFrame(my_ip, friend_ip, None, title="chat_frame")
        self.main_frame.pop_chat_window_list.append(chat_frame)
        chat_frame.Show()


class GroupPanel(wx.Panel):
    """
    创建用户组列表的panel
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class MainFrame(wx.Frame):
    """
    程序的主窗口，运行程序后程序展示的画面；
    """
    def __init__(self, *args, **kwargs):
        # ensure the parent's __init__ is called.
        super(self.__class__, self).__init__(*args, **kwargs)
        # 启动端口监听,将收到的卡片保存在用户表单中，若是收到的是用户的信息则发给对应的聊天窗口；
        # 当程序启动时，使用UDP协议向255.255.255.255这个广播地址发送广播包,默认端口是44444。
        self.usr_sheet = UserSheet()
        self.ip = self.usr_sheet.get_ip()
        self.message_list = []
        self.pop_chat_window_list = []
        self.listener = Listener(self)
        self.listener.setDaemon(True)
        self.listener.start()
        # Set the window's size
        self.SetMaxSize((MAIN_WIN_WIDTH, MAIN_WIN_HIGH))
        self.SetMinSize((MAIN_WIN_WIDTH, MAIN_WIN_HIGH))
        # set Icon
        self.icon_img_path = os.path.abspath("./images/Icon_v0.1.png")
        self.icon = wx.Icon(self.icon_img_path, type=wx.BITMAP_TYPE_ANY)
        self.SetIcon(self.icon)
        # create a panel in the frame
        self.windowpanel = wx.Panel(self)

        # 添加头像 50* 50
            # 载入图像
        profile_photo = wx.Image("./images/profile_photo_v0.1.png", wx.BITMAP_TYPE_ANY)
            # 缩放图像
            # 转换它们为静态位图部件
        self.sbm_profile = wx.StaticBitmap(self.windowpanel, -1, wx.BitmapFromImage(profile_photo))
        self.sbm_profile.Bind(wx.EVT_LEFT_DCLICK, self.OnChangeprofilegraph)
        # put them into the sizer

        # 添加状态图标和文字
        list_status = ['在线', '忙', '离线']
        self.combo_box_1 = wx.ComboBox(self.windowpanel, -1, value='在线', choices=list_status, style=wx.CB_SORT)

        # 添加事件处理；
        self.Bind(wx.EVT_COMBOBOX, self.OnConbobox, self.combo_box_1)

        # 添加计算机名称
        self.host_name = HOST_NAME
            # 使用 wx.lib.stattext.GenStaticText
            # self.hname = wx.StaticText(self.windowpanel, label=self.host_name)
        self.hname = GenStaticText(self.windowpanel, -1, label=self.host_name)
        self.hname.Bind(wx.EVT_LEFT_DCLICK, self.OnChangehostname)

        # 添加个性签名
        profile_sign = '编辑个性签名'
        # self.psign = wx.StaticText(self.windowpanel, label=profile_sign)
            # wx.StaticText 是c++写的原生控件，不支持鼠标事件，而wx.lib.stattext.GenStaticText
            # 是使用python重写的一个静态文本控件，支持鼠标事件。
        self.psign = GenStaticText(self.windowpanel, -1, label=profile_sign)
            # 下面代码没有效果。 鼠标的事件应该绑定到具体的组件上而不是框架上。
            # self.Bind(wx.EVT_LEFT_DCLICK, self.OnChangehostname, self.hname)
        self.psign.Bind(wx.EVT_LEFT_DCLICK, self.OnChangepsign)

        # 添加搜索栏
        self.search_bar = wx.TextCtrl(self.windowpanel, -1, "Search friends!")
            # 当输入用户名后，回车返回搜索到的好友。

        # 添加用户列表notebook。
            # 使用notebook控件来达到用户列表，组列表的多标签窗口；
            # 如何使用notebook控件: 如下，定义不同的面板类，添加到多标签窗口中.
        self.note_book = wx.Notebook(self.windowpanel)
        self.note_book.AddPage(UsrsPanel(self.note_book, self), "用户列表")
        self.note_book.AddPage(GroupPanel(self.note_book), "用户组列表")
        self.note_book.AddPage(UsrSheetShow(self.usr_sheet, self.note_book), "用户组列表2")


        # 测试函数用按钮
        self.testhostname = wx.Button(self.windowpanel, -1, "testhostname")
        self.Bind(wx.EVT_BUTTON, self.OnChangehostname, self.testhostname)


        # layout
        # 主要布局
        mainbox = wx.BoxSizer(wx.VERTICAL)
        # 个人信息状态布局
        headsizer = wx.GridBagSizer(hgap=10, vgap=10)
        headsizer.Add(self.sbm_profile, pos=(0, 0), span=(2, 1), flag=wx.EXPAND)
        headsizer.Add(self.combo_box_1, pos=(0, 1))
        headsizer.Add(self.hname, pos=(0, 2))
        headsizer.Add(self.psign, pos=(1, 1), span=(1, 2))
        headsizer.Add(self.search_bar, pos=(2, 0), span=(1, 3), flag=wx.EXPAND)
        # 使最后的行和列可增长。
        headsizer.AddGrowableCol(2)
        headsizer.AddGrowableRow(2)
        mainbox.Add(headsizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # 用户列表布局
        # usrs_sizer = wx.BoxSizer()
        # usrs_sizer.Add(self.note_book)
        # mainbox.Add(usrs_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        # 使用上面三行代码会导致notebook控件不能向两边自动扩充，而是根据内容实际的尺寸。
        mainbox.Add(self.note_book, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # 用于测试按钮的布局
        testsizer = wx.BoxSizer()
        testsizer.Add(self.testhostname)
        mainbox.Add(testsizer)

        self.windowpanel.SetSizer(mainbox)
        self.windowpanel.Fit()


    def OnChangeprofilegraph(self, event):
        """
        双击头像控件时，弹出图片文件选择对话框，更改图片。
        :param event:
        :return: None
        """
        print("ok")
        return None

    def OnConbobox(self, event):
        """
        当更改状态时触发。
        :param event:
        :return:
        """
        print('hello')

    def OnChangehostname(self, event):
        """
        当双击主机名称时触发，用来更改主机的名称。
        :param event:
        :return: None
        """
        text_entry_dialog = wx.TextEntryDialog(None, "请输入主机名称：", "编辑主机名称", "主机名称")
        if text_entry_dialog.ShowModal() == wx.ID_OK:
            host_name = text_entry_dialog.GetValue()
            if host_name == "":
                host_name = HOST_NAME
        else:
            host_name = HOST_NAME
        self.hname.SetLabel(host_name)
        return None

    def OnChangepsign(self, event):
        """
        当双击个性签名时触发，用来更改个性签名。
        :param event:
        :return: None
        """
        texentrydialog = wx.TextEntryDialog(None, "请输入个性签名：", "编辑个性签名", "个性签名")
        if texentrydialog.ShowModal() == wx.ID_OK:
            psing = texentrydialog.GetValue()
            if psing == "":
                psing = HOST_NAME
        else:
            psing = HOST_NAME
        self.psign.SetLabel(psing)
        return None

    def pop_chat_window(self, event):
        """
        聊天时调用次方法弹出聊天窗口；
        :return: None
        """
        pass


class ChatFrame(wx.Frame):
    """
    聊天窗口，和特定用户聊天时弹出的窗口；
    需要将弹出窗口的用户id(本机id，对方id）传过来并使用对方ID使用最为唯一标识这个窗口
    问题1：聊天chuang'k
    """
    def __init__(self, my_ip, friend_ip, *args, **kwargs):
        super(ChatFrame, self).__init__(*args, **kwargs)
        self.SetMinSize((CHAT_WIN_WIDTH, CHAT_WIN_HIGH))
        self.SetMaxSize((CHAT_WIN_WIDTH, CHAT_WIN_HIGH))
        # 此处应该将此窗口本机ip和聊天对方的ip绑定到ChatFrame实例中，用来唯一标识这个聊天窗口实例；
        self.my_ip = my_ip
        self.friend_ip = friend_ip
        # st = wx.StaticText(panel_window, label="聊天窗口")
        main_box = wx.BoxSizer(wx.VERTICAL)
        msg_panel = wx.Panel(self)
        self.gbs = wx.GridBagSizer(hgap=10, vgap=10)
        self.chat_record_show = wx.TextCtrl(msg_panel, -1, style=wx.EXPAND | wx.TE_MULTILINE |
                                                                 wx.TE_READONLY | wx.TE_AUTO_URL)
        self.msg_enter_box = wx.TextCtrl(msg_panel, -1, style=wx.EXPAND | wx.TE_MULTILINE)

        self.send_button = wx.Button(msg_panel, -1, label="发送", name="send")
        self.Bind(wx.EVT_BUTTON, self.OnSendMsg, self.send_button)
        self.gbs.Add(self.chat_record_show, pos=(0, 0), span=(1, 2), flag=wx.EXPAND)
        self.gbs.Add(self.msg_enter_box, pos=(1, 0), span=(1, 1), flag=wx.EXPAND)
        self.gbs.Add(self.send_button, pos=(1, 1), span=(1, 1), flag=wx.EXPAND)
        self.gbs.AddGrowableRow(0)
        self.gbs.AddGrowableCol(0)
        main_box.Add(self.gbs, 1, flag=wx.EXPAND | wx.ALL, border=10)
        msg_panel.SetSizerAndFit(main_box)

    def OnSendMsg(self, event):
        msg = self.msg_enter_box.GetValue()
        send_msg = f"message#{self.my_ip}#{self.friend_ip}#{msg!r}"
        self.SendMsg(send_msg)
        show_msg = send_msg
        self.ShowMsg(show_msg)

    def SendMsg(self, send_msg):
        print(send_msg.split("#")[2])
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(send_msg.encode(ENCODING), (send_msg.split("#")[2], 44444))
        udp_socket.close()

    def ShowMsg(self, show_msg):
        send_ip = show_msg.split("#")[1]
        msg = str(show_msg.split('#')[3])
        if send_ip == self.my_ip:
            show_msg_text = f"我：\n{msg[1:-1]}\n\n"
            self.msg_enter_box.Clear()
        else:
            show_msg_text = f"{send_ip}\n{msg[1:-1]}"
        self.chat_record_show.write(show_msg_text)


class MmcqApp(wx.App):
    """
    程序界面APP
    """

    def __init__(self, *args, **kwargs):
        # equal to 'super(MmcqApp, self).__init__(*args, **kwargs)'
        super(self.__class__, self).__init__(*args, **kwargs)

    def OnInit(self):
        self.mainfrm = MainFrame(None, title=WIN_TITLE)
        self.mainfrm.Show()
        return True

    def OnExit(self):
        """
          wx.App子类的OnExit()方法在最后一个窗口被关闭且在wxPython的内在清理过程之前被调用，
          所以，可以在OnExit()方法中清理任何创建的非wxPython资源。
          如果调用了wx.Exit()关闭wxPython程序，OnExit()方法仍会被调用。
        """
        self.mainfrm.listener

        pass


def main():
    app = MmcqApp()
    app.MainLoop()


if __name__ == '__main__':
    """
    用于测试
    """
    main()
