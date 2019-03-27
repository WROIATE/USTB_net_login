import psutil,time


class info():
	def __init__(self):
		self.dtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		
	def netspeed(self):
		p = psutil.net_io_counters()
		time.sleep(1)
		n = psutil.net_io_counters()
		speed = '%.2f'%((n[1]-p[1])/1024)
		return str(speed)
