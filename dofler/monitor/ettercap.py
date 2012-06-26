from base import BaseParser
import re
import dofler.api.client

class Parser(BaseParser):
	'''The Ettercap password parser.'''
	ruser = re.compile(r'USER: (.*?)  ')	# USER Regex: Pulls out USER field.
	rpass = re.compile(r'PASS: (.*?)  ')	# PASS Regex: Pulls out PASS field.
	rinfo = re.compile(r'INFO: (.*?)$')		# INFO Regex: Pulls out INFO field.
	promisc = {True: '', False: '-p'}		# Promiscuous flags.
	cmd = 'ettercap {PROMISC} -Tzuqi {INTERFACE}'	# Command to run.

	def parse(self, line):
		'''Ettercap line output parser.'''
		if 'USER' in line:

			usernames = self.ruser.findall(line)
			passwords = self.rpass.findall(line)
			infos = self.rinfo.findall(line)

			if len(usernames) > 0 and len(passwords) > 0:
				username = usernames[0]
				password = passwords[0]
				info = infos[0]
				dofler.api.client.account(username, passowrd, 
										  info, proto, 'ettercap')		