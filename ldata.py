import sys,os
import json
from io import StringIO

class datA():
	def __init__(self):
		self.ospath = os.path.abspath('.')
		self.file_path = os.path.join(self.ospath, 'file')
		self.pw_path = os.path.join(self.file_path, 'pw.json')
		self.auto_path = os.path.join(self.file_path, 'auto.json')
		self.common  = {
						'DDDDD' :'',
						'upass' :'',
						'v6ip'  :'',
						'0MKKey':'123456789'
						}
						
		self.setting = {
						'auto':False,
						'save':False
						}
		self.creatpath()
		
	def creatpath(self):
		if not os.path.exists(self.file_path):
			os.makedirs(self.file_path)
		if not os.path.exists(self.pw_path):
			with open(self.pw_path,'w') as g:
				json.dump(self.common,g)
		if not os.path.exists(self.auto_path):
			with open(self.auto_path,'w') as f:
				json.dump(self.setting,f)
	
	def read_pw(self):
		d = ''
		with open(self.pw_path,'r') as f:
			d = json.load(f);
		return d
	
	def read_setting(self):
		d = ''
		with open(self.auto_path,'r') as f:
			d = json.load(f);
		return d

	def write_pw(self,dict):
		with open(self.pw_path,'w') as f:
			json.dump(dict,f)
		
	def write_setting(self,dict):
		with open(self.auto_path,'w') as f:
			json.dump(dict,f)
			
	def reset(self):
		with open(self.pw_path,'w') as f:
			json.dump(self.common,f)
		with open(self.auto_path,'w') as f:
			json.dump(self.setting,f)
			
if __name__ == "__main__":
	a = datA()