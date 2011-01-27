import os
import threading
import time
import Queue

from Module import IModule, Module, ModuleArgument
from User import User, Authentication

class admin (IModule):
	def __init__(self, queue):
		self.queue = queue
		self.DataStore = dict()
		self.Authentication = Authentication()
		threading.Thread.__init__ ( self )
	
	def run(self):
		while True:
			arg = self.queue.get()
			if arg.Name == "Initialize":
				arg.Arg.Commands.append("privmsg")
				arg.Arg.NeedsBot = True
				self.bot = None
			elif arg.Name == "privmsg":
				if self.bot == None:
					self.bot = arg.AuxData
				self.privmsg(arg.Arg, arg.Data)
			elif arg.Name == "die":
				break
	
	def privmsg(self, network, data):
		parsed = self.GetParts(data)
		
		if parsed["Arguments"][0][0] == ".":
			if parsed["Arguments"][0] == ".admin":
				self.admin(network, parsed)
	
	def admin(self, network, parsed):
		arguments = parsed["Arguments"]
		if arguments[1] == "login":
			if len(arguments) < 4:
				network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Denied!\r\n")
				return
			
			self.login(network, parsed)
		elif arguments[1] == "networks":
			self.networks(network, parsed)
		elif arguments[1] == "roles":
			self.roles(network, parsed)
		elif arguments[1] == "join":
			self.join(network, parsed)
		elif arguments[1] == "part":
			self.part(network, parsed)
	
	def login(self, network, parsed):
		if self.Authentication.NeedsAuthentication(network, parsed["Arguments"][2]) == False:
			# Anonymous access not allowed for administration
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Authentication unsuccessful\r\n")
			return
		
		if self.Authentication.AuthenticateUser(network, parsed["Arguments"][2], parsed["Arguments"][3]) == True:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Authentication successful\r\n")
		else:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Authentication unsuccessful\r\n")
	
	def roles(self, network, parsed):
		roles = ""
		
		for role in self.Authentication.GetAuthenticatedUser(network, parsed["FromWhom"]).Roles:
			if roles == "":
				roles = role
			else:
				roles += ", " + role
		
		network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :You are in the following roles: " + roles + "\r\n")
	
	def join(self, network, parsed):
		if "Admin" in self.Authentication.GetAuthenticatedUser(network, parsed["FromWhom"]).Roles:
			network.JoinChannel(parsed["Arguments"][2])
	
	def part(self, network, parsed):
		if "Admin" in self.Authentication.GetAuthenticatedUser(network, parsed["FromWhom"]).Roles:
			network.PartChannel(parsed["Arguments"][2])
	
	def networks(self, network, parsed):
		user = self.Authentication.GetAuthenticatedUser(network, parsed["FromWhom"])
		allowed_networks = list()
		if "SuperAdmin" in user.Roles:
			for n in self.bot.networks:
				allowed_networks.append(n)
		elif "Admin" in user.Roles:
			allowed_networks.append(network)
			
		for n in allowed_networks:
			active = "False"
			if n.Output != None:
				active = "True"
			
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :[" + n.Name + "]\r\n")
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :    -> Hostname:port = " + n.Hostname +  ":" + repr(n.Port) + "\r\n")
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :    -> Active = " + active + "\r\n")
