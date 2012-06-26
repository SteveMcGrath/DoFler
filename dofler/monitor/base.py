import threading
import re
import sys
import time
import pexpect

class BaseParser(threading.Thread):
	'''This is the base class that all parsers inherit.  All of the process
	management is already handled here and some basic function stubs are 
	provided as a starting point for parsing the application output.
	'''
	breaker = False					# The breaker flag.  If set to true will
									# cause the thread to bottom out.
	promisc = {True: '', False: ''} # The promiscuous flag settings.  As this
									# vary from app to app, this is set
									# dependent on this dictionary.
	cmd = ''						# The child process command.

	def run(self, interface, timer=1800, promisc=False):
		'''Required function for threading.
		'''
		self.svc(interface, timer)


	def svc(self, interface, timer, promisc):
		'''The service manager for the thread.  This is where the child
		process is actually being spawned and maintained.
		'''
		start = time.time()		# Set the start timer

		# Replace the options in the command with the interface and promiscuous
		# settings as needed.
		cmd = self.cmd.replace('{INTERFACE}', interface)\
					  .replace('{PROMISC}', self.promisc[promisc])

		# Yeah! Loops!
		while not self.breaker:

			# Here we actually start the child process and then run through the
			# output in a loop until either the process exits, the timer hits,
			# or someone sets the breaker flag.
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

			# As we either broke out of the process or the timer hit, lets make
			# sure to terminate the process and reset the timer to the current
			# time.
			p.terminate()
			start = time.time()


	def parse(self, line):
		'''A simple parser for the base model'''
		print line.strip('\r\n')
		