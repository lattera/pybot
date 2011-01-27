import os
import threading
import time
import Queue

from Module import IModule, Module, ModuleArgument
from User import User, Authentication

class stats (IModule):
	def __init__(self, queue):
		self.queue = queue
		self.pisg = "/export/home/shawn/Downloads/irc/pisg-0.72/pisg"
		self.Authentication = Authentication()
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
			
		if parsed["Arguments"][0] == ".stats":
			if len(parsed["Arguments"]) < 2:
				network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Please give me some arguments\r\n")
				return
			
			if parsed["Arguments"][1] == "gen":
				self.genstats(network, parsed)
				return
			
			if parsed["Arguments"][1] == "login":
				self.login(network, parsed)
				return
	
	def login(self, network, parsed):
		if len(parsed["Arguments"]) < 4:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Denied!\r\n")
			return
		
		if self.Authentication.NeedsAuthentication(network, parsed["FromWhom"]) == False:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Denied!\r\n")
			return
		
		if self.Authentication.AuthenticateUser(network, parsed["Arguments"][2], parsed["Arguments"][3]) == False:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Denied!\r\n")
			return
		
		network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Granted!\r\n")
	
	def genstats(self, network, parsed):
		if not "User" in self.Authentication.GetAuthenticatedUser(network, parsed["FromWhom"]).Roles:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Denied!\r\n")
			return
		
		network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Generating stats\r\n")
		os.system(self.pisg)
		network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Generation of stats done\r\n")
