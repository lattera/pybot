import os
import threading
import time
import Queue

from Module import IModule, Module, ModuleArgument
from User import User, Authentication

class log (IModule):
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
		realmessage = data[data.find(parsed["Arguments"][0]):]
		realtime = time.asctime()
		
		parsedtime = realtime[4:-4]
		
		f = open("logs/" + network.Name + "-" + parsed["ToWhom"] + ".log", "a+")
		if len(realmessage) >= len("ACTION") and realmessage[1:len("ACTION")+1] == "ACTION" and realmessage[0] == "\x01":
			f.write(parsedtime + "*\t" + parsed["FromWhom"] + " " + realmessage[len("ACTION")+2:-1] + "\n")
		else:
			f.write(parsedtime + "<" + parsed["FromWhom"] + "> " + realmessage + "\n")
		f.close()
