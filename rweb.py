import requests
import re
from bs4 import BeautifulSoup

class login():
	def __init__(self):
		self.loginurl = 'http://202.204.48.66/'
		self.checkurl = 'http://cippv6.ustb.edu.cn/get_ip.php'
		self.ipv6 = ''
		self.checkweb()
		
		
	def checkweb(self):
		try:
			r = requests.get(self.loginurl,timeout=2)
			r.raise_for_status()
		except:
			return False
		try:
			p = requests.get(self.checkurl,timeout=2)
			p.raise_for_status()
			self.ipv6 = re.findall("'(.+?)'",p.text)[0]
		except:
			return True
		
		
	def trs(self,flow):
		flow = int(flow)
		flow0=flow%1024
		flow1=flow-flow0
		flow0=flow0*1000
		flow0=flow0-flow0%1024
		flow3='.'
		if(flow0/1024<10):
			flow3='.00'
		elif(flow0/1024<100):
			flow3='.0'
		return str(int(flow1/1024))+flow3+str(round(flow0/1024))
		
		
	def repost(self,dict):
		userData = dict
		try:
			userData['v6ip'] = self.ipv6
			m = requests.post(self.loginurl,data=userData)
			t = requests.get('https://www.baidu.com/',timeout = 2)
			t.raise_for_status()
		except:
			return False
		return True
	
	
	def getmsg(self):
			r = requests.get(self.loginurl,timeout=2)
			r.raise_for_status()
			msg = BeautifulSoup(r.content,'lxml')
			msg = msg.script.get_text()
			Msg = re.findall(r'(\')([\d\s]{10})(\')',msg)
			ip4 = re.search(r'(v4ip=\')(\S+)(\';v6ip)',msg)[2]
			ip6 = re.search(r'(v6ip=\')(\S+)(\';//)',msg)[2]
			m6 = re.search(r'(v6af=)(\d+)(;)',msg)[2]
			list = ['0','0','0','0','0','0']
			cou = 0
			for i in Msg:
				list[cou] = i[1].rstrip()
				cou += 1
			list[0] = list[0]
			list[1] = str(self.trs(list[1]))
			list[2] = str((float(list[2]) - float(list[2])%100)/10000)
			list[3] = ip4
			list[4] = ip6
			list[5] = str('%.2f'%(float(m6)/4096))
			return list

			
if __name__ == "__main__":
	a = login()
	a.repost({})
	print(a.getmsg())
