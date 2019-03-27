import rweb
import ldata,info
import wx,time
import wx.adv
import sys,os,threading
import win32api,win32con
from io import StringIO
from multiprocessing import Process

un  = StringIO()
up  = StringIO()
APP_TITLE = u'校园网登录程序'
APP_ICON = 'res/python.ico'


class MyTaskBarIcon(wx.adv.TaskBarIcon):
	ICON = 'res/python.ico'  # 图标地址
	ID_ABOUT = 1  # 菜单选项“关于”的ID
	ID_EXIT = 2  # 菜单选项“退出”的ID
	ID_SHOW_WEB = 3  # 菜单选项“显示页面”的ID
	TITLE = 'ustb网络助手' #鼠标移动到图标上显示的文字

	def __init__(self,frame):
		wx.adv.TaskBarIcon.__init__(self)
		self.window = frame
		self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
		self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)  # 绑定“关于”选项的点击事件
		self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)  # 绑定“退出”选项的点击事件
		self.Bind(wx.EVT_MENU, self.onShowWeb, id=self.ID_SHOW_WEB)  # 绑定“显示页面”选项的点击事件


	# “关于”选项的事件处理器
	def onAbout(self, event):
		wx.MessageBox('程序作者：WROIATE 2019.3.23', "关于")

	# “退出”选项的事件处理器
	def onExit(self, event):
		self.window.close()
		self.Destroy()

	# “显示页面”选项的事件处理器
	def onShowWeb(self, event):
		self.window.Show()

	# 创建菜单选项
	def CreatePopupMenu(self):
		menu = wx.Menu()
		for mentAttr in self.getMenuAttrs():
			menu.Append(mentAttr[1], mentAttr[0])
		return menu

		# 获取菜单的属性元组
	def getMenuAttrs(self):
		return [('进入程序', self.ID_SHOW_WEB),
				('关于', self.ID_ABOUT),
				('退出', self.ID_EXIT)]

class mainFrame(wx.Frame):
	'''程序主窗口类，继承自wx.Frame'''
 
	def __init__(self, parent):
		'''构造函数'''
		wx.Frame.__init__(self, parent, -1, APP_TITLE)
		self.SetBackgroundColour(wx.Colour(224, 224, 224))
		self.SetSize((520, 240))
		self.Center()
		self.data      =    ldata.datA()
		self.net       =    rweb.login()
		self.info      =    info.info()
		self.state_2   =    False
		self.state_1   =    False
		self.state     =    False
		self.list      =    {'余额':'','时间':'','4流量':'','6流量':'','ip4':'','ip6':'none','speed':''}
		self.sped      =    threading.Thread(target = self.speed, name = 'speed')
		self.bar       =    MyTaskBarIcon(self)#显示系统托盘图标


 
		if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
			exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
			icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
		else :
			icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon)

		self.tip   = wx.StaticText(self, -1, u'', pos=(120, 160), size=(150, -1), style=wx.ALIGN_LEFT)
		self.tip2  = wx.StaticText(self, -1, u'', pos=(120, 20), size=(150, -1), style=wx.ALIGN_LEFT)
		self.tip3  = wx.StaticText(self, -1, u'', pos=(120, 40), size=(150, -1), style=wx.ALIGN_LEFT)
		self.tip4  = wx.StaticText(self, -1, u'', pos=(120, 60), size=(150, -1), style=wx.ALIGN_LEFT)
		self.tip5  = wx.StaticText(self, -1, u'', pos=(120, 80), size=(150, -1), style=wx.ALIGN_LEFT)
		self.tip6  = wx.StaticText(self, -1, u'', pos=(120, 100), size=(150, -1), style=wx.ALIGN_LEFT)
		self.tip7  = wx.StaticText(self, -1, u'', pos=(120, 120), size=(150, -1), style=wx.ALIGN_LEFT)
		self.tip8  = wx.StaticText(self, -1, u'', pos=(120, 140), size=(150, -1), style=wx.ALIGN_LEFT)
		self.txt_1 = wx.StaticText(self, -1, u'账号：', pos=(40, 50), size=(100, -1), style=wx.ALIGN_RIGHT)
		self.txt_2 = wx.StaticText(self, -1, u'密码：', pos=(40, 80), size=(100, -1), style=wx.ALIGN_RIGHT)

		self.tc1 = wx.TextCtrl(self, -1, '', pos=(145, 50), size=(150, -1), name='TC01', style=wx.TE_LEFT)
		self.tc2 = wx.TextCtrl(self, -1, '', pos=(145, 80), size=(150, -1), name='TC02', style=wx.TE_PASSWORD|wx.ALIGN_LEFT)

		self.btn_mea = wx.Button(self, -1, u'记住', pos=(350, 50), size=(100, 25))
		self.btn_meb = wx.Button(self, -1, u'登录', pos=(350, 80), size=(100, 25))
		self.btn_close = wx.Button(self, -1, u'自动登录', pos=(350, 110), size=(100, 25))
 
		# 控件事件
		self.tc1.Bind(wx.EVT_TEXT, self.EvtText)
		self.tc2.Bind(wx.EVT_TEXT, self.EvtText)

 
		# 鼠标事件 
		self.btn_mea.Bind(wx.EVT_LEFT_UP, self.OnLeftUp1)
		self.btn_meb.Bind(wx.EVT_LEFT_UP, self.OnLeftUp2)
		self.btn_close.Bind(wx.EVT_LEFT_UP, self.autologin)
		
 
		# 键盘事件
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
 
		# 系统事件
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_SIZE, self.On_size)
		#self.Bind(wx.EVT_PAINT, self.On_paint)
		#self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
		self.mkdir()
 
	def EvtText(self, evt):
		'''输入框事件函数'''
		obj = evt.GetEventObject()
		objName = obj.GetName()
		if objName == 'TC01':
			pass
		elif objName == 'TC02':
			pass
		
	def speed(self):
		while self.state_2 == True:
			self.list['speed'] = self.info.netspeed()
			self.tip4.SetLabel('当前下载网速：'+self.list['speed']+'kB/s')
			self.bar.SetIcon(wx.Icon(self.bar.ICON),'当前下载网速：'+self.list['speed']+'kB/s')
			
	def autologin(self, evt):
		if self.state_1:
			dlg = wx.MessageDialog(None, u'已取消自动登录', u'操作提示')
			if dlg.ShowModal() == wx.ID_OK:
				self.state_1 = False
			self.tip.SetLabel(u'已取消自动登录')
		else:
			
			dlg = wx.MessageDialog(None, u'已设为自动登录，密码默认记住', u'操作提示')
			if dlg.ShowModal() == wx.ID_OK:
				self.state = True
				self.state_1 = True
			self.tip.SetLabel(u'已设为自动登录')
		
		
	def On_size(self, evt):
		'''改变窗口大小事件函数'''
		self.Refresh()
		evt.Skip()
 
	def OnClose(self, evt):
		'''关闭窗口事件函数'''
		dlg = wx.MessageDialog(None, u'是否缩小到托盘？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
		if(dlg.ShowModal() == wx.ID_YES):
			self.Hide()
		else:
			dict = self.data.read_setting()
			dict['save'] = self.state
			dict['auto'] = self.state_1
			self.data.write_setting(dict)
			if self.data.read_setting()['save']:
				self.data.write_pw(self.wri())
			else:
				self.data.reset()
			if self.state_2 == True:
				self.state_2 = False
				self.sped.join(1)
			'''我靠是真的蛋疼，这个state_2不会马上传到线程函数里，
			然后join又会立刻把主线程停住进入死循环(?)，我只能想到用挂起了'''
			wx.Exit()
 
	def close(self):
		'''这边我解决不了了。。。'''
		self.state_2 = False
		dict = self.data.read_setting()
		dict['save'] = self.state
		dict['auto'] = self.state_1
		self.data.write_setting(dict)
		if self.data.read_setting()['save']:
			self.data.write_pw(self.wri())
		else:
			self.data.reset()
		self.sped.join(1)
		self.Destroy()
		
	def OnLeftUp1(self, evt):
		'''左键弹起事件1函数'''
		if self.state:
			dlg = wx.MessageDialog(None, u'已取消保存', u'操作提示')
			if dlg.ShowModal() == wx.ID_OK:
				self.state = False
				self.state_1 = False
			self.tip.SetLabel(u'已取消保存')
		else :
			dlg = wx.MessageDialog(None, u'密码已记住', u'操作提示')
			if dlg.ShowModal() == wx.ID_OK:
				self.state = True
			self.tip.SetLabel(u'密码已记住')
 
	def OnLeftUp2(self, evt):
		'''左键弹起事件2函数'''
		self.tip.SetLabel(u'正在登陆')
		if self.net.repost(self.wri()):
			self.get_msg()
			dlg = wx.MessageDialog(None, u'登陆成功', u'操作提示')
			if(dlg.ShowModal() == wx.ID_OK):
				self.show_0()
				self.sped.start()
		else:
			if self.state_1:
				self.state = True
				self.state_1 = False
			dlg = wx.MessageDialog(None, u'登陆失败，请检查网络或输入信息', u'操作提示')
			if dlg.ShowModal() == wx.ID_OK:
				self.tip.SetLabel(u'登陆失败')

 
	def OnMouse(self, evt):
		'''鼠标事件函数'''
		self.tip.SetLabel(str(evt.EventType))
		
	def OnKeyDown(self, evt):
		'''键盘事件函数'''
		key = evt.GetKeyCode() 
		self.tip.SetLabel(str(key))

	def mkdir(self): 
		dict           =   self.data.read_setting()
		self.state     =   dict['save']
		self.state_1   =   dict['auto']
		
		if self.net.repost({}):
			self.get_msg()
			dlg = wx.MessageDialog(None, u'网络已处于连接状态', u'操作提示')
			if(dlg.ShowModal() == wx.ID_OK):
				sub = self.data.read_pw()
				self.tc1.write(sub['DDDDD'])
				self.tc2.write(sub['upass'])
				self.show_0()
				self.sped.start()
		
		elif dict['auto']:
			sub = self.data.read_pw()
			self.tc1.write(sub['DDDDD'])
			self.tc2.write(sub['upass'])
			if not self.net.repost(sub):
				self.state_1 = False
				dlg = wx.MessageDialog(None, u'登陆失败，请检查网络或输入信息', u'操作提示')
				if dlg.ShowModal() == wx.ID_OK:
					self.tip.SetLabel(u'登陆失败')
					self.hide_0()
			else:
				self.get_msg()
				self.hide_0()
				self.show_0()
				self.sped.start()
		elif dict['save']:
			sub = self.data.read_pw()
			self.tc1.write(sub['DDDDD'])
			self.tc2.write(sub['upass'])
			self.hide_0()
		else:
			self.hide_0()
					
	
	def wri(self):
		common          = self.data.read_pw()
		common['DDDDD'] = self.tc1.GetValue()
		common['upass'] = self.tc2.GetValue()
		return common
		
	def get_msg(self):
		msg = self.net.getmsg()
		self.list['余额']  = '当前余额：'    +msg[2]+ '元'
		self.list['4流量'] = 'v4流量：'      +msg[1]+ 'MB'
		self.list['时间']  = '已用时间：'    +msg[0]+ '分钟'
		self.list['6流量'] = 'v6流量：'      +msg[5]+ 'MB'
		self.list['ip4']   = '当前ipv4地址：'+msg[3]
		self.list['ip6']   = '当前ipv6地址：'+msg[4]
 
	def show_0(self):
		self.tc1.Hide()
		self.tc2.Hide()
		self.txt_1.Hide()
		self.txt_2.Hide()
		self.btn_mea.Hide()
		self.btn_meb.Hide()
		self.btn_close.Hide()
		self.tip.SetLabel('登陆成功')
		self.tip2.SetLabel(self.list['余额'])
		self.tip3.SetLabel(self.list['时间'])
		self.tip5.SetLabel(self.list['4流量'])
		self.tip6.SetLabel(self.list['6流量'])
		self.tip7.SetLabel(self.list['ip4'])
		self.tip8.SetLabel(self.list['ip6'])
		self.tip2.Show()
		self.tip3.Show()
		self.tip4.Show()
		self.tip5.Show()
		self.tip6.Show()
		self.tip7.Show()
		self.tip8.Show()
		self.state_2 = True

	def hide_0(self):
		self.tip2.Hide()
		self.tip3.Hide()
		self.tip4.Hide()
		self.tip5.Hide()
		self.tip6.Hide()
		self.tip7.Hide()
		self.tip8.Hide()

 
class mainApp(wx.App):
	def OnInit(self):
		self.SetAppName(APP_TITLE)
		self.Frame = mainFrame(None)
		self.Frame.Show()#显示主界面
		return True
 
if __name__ == "__main__":
	app = mainApp()
	app.MainLoop()