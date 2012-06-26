import threading
import re
import sys
import time
import pexpect

class BaseParser(threading.Thread):
	ruser = re.compile(r'USER: (.*?)')
	rpass = re.compile(r'PASS: (.*?)')
	rinfo = re.compile(r'INFO: (.*?)')
	breaker = False
	cmd = []

	def run(self, interface, timer=1800):
		self.svc(interface, timer)


	def svc(self, interface, timer):
		start = time.time()
		cmd = self.cmd.replace('{INTERFACE}', interface)
		while not self.breaker:
			p = pexpect.spawn(cmd)
			while not self.breaker and (int(time.time()) - int(start)) < timer:
				try:
					line = p.readline()
					if line == '':
						if p.poll() is not None:
							time.sleep(0.1)
						else:
							break
					else:
						self.parse(line)
				except pexpect.TIMEOUT:
					pass
			p.terminate()


	def parse(self, line):
		print line.strip('\r\n')
		