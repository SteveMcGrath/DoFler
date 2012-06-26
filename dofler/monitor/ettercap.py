from base import BaseParser
import re
#from dofler.client import API

class Parser(BaseParser):
	ruser = re.compile(r'USER: (.*?)  ')
	rpass = re.compile(r'PASS: (.*?)  ')
	rinfo = re.compile(r'INFO: (.*?)$')
	cmd = 'ettercap -Tzuqpi {INTERFACE}'

	def parse(self, line):
		print line
		if 'USER' in line:
			usernames = self.ruser.findall(line)
			passwords = self.rpass.findall(line)
			infos = self.rinfo.findall(line)

			if len(usernames) > 0 and len(passwords) > 0:
				username = usernames[0]
				password = passwords[0]
				info = infos[0]
				print 'ettercap', username, password, info
		