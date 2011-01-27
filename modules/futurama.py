import os
import threading
import time
import Queue

from Module import IModule, Module, ModuleArgument

class futurama (IModule):
	def __init__(self, queue):
		self.queue = queue
		threading.Thread.__init__ ( self )
	
	def run(self):
		while True:
			arg = self.queue.get()
			if arg.Name == "Initialize":
				arg.Arg.Commands.append("privmsg")
			elif arg.Name == "privmsg":
				self.privmsg(arg.Arg, arg.Data)
			elif arg.Name == "die":
				break
	
	def privmsg(self, network, data):
		parsed = self.GetParts(data)
		if parsed["Arguments"][0] == ".futurama":
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :" + os.popen("curl -Is slashdot.org|grep 'X'|tail -n 3|head -n 1|cut -b 03-").readline().strip() + "\r\n")
