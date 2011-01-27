# -*- coding: utf-8 -*-
import os
import threading
import time
import Queue

from googlevoice import Voice

from Module import IModule, Module, ModuleArgument
from User import User, Authentication

class gvoice (IModule):
	def __init__(self, queue):
		self.queue = queue
		
		self.voice = Voice()
		self.voiceLoggedIn = False
		
		self.Authentication = Authentication()
		threading.Thread.__init__ ( self )
	
	def run(self):
		while True:
			arg = self.queue.get()
			if arg.Name == "Initialize":
				arg.Arg.Commands.append("privmsg")
				arg.Arg.Commands.append("part")
				arg.Arg.Commands.append("quit")
			elif arg.Name == "privmsg":
				self.privmsg(arg.Arg, arg.Data)
			elif arg.Name == "part":
				self.part(arg.Arg, arg.Data)
			elif arg.Name == "join":
				self.part(arg.Arg, arg.Data)
			elif arg.Name == "quit":
				self.part(arg.Arg, arg.Data)
			elif arg.Name == "nick":
				self.part(arg.Arg, arg.Data)
			elif arg.Name == "die":
				break
	
	def privmsg(self, network, data):
		parsed = self.GetParts(data)
			
		if parsed["Arguments"][0] == ".gvoice":
			if len(parsed["Arguments"]) < 2:
				network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Please give me some arguments\r\n")
				return
			
			if parsed["Arguments"][1] == "sms":
				self.sms(network, parsed, data)
				return
			
			if parsed["Arguments"][1] == "login":
				self.login(network, parsed)
				return
	
	def part(self, network, data):
		parsed = self.GetParts(data)
		
		self.Authentication.DeauthenticateUser(network, parsed["FromWhom"])
	
	def sms(self, network, parsed, raw):
		if not "Voice" in self.Authentication.GetAuthenticatedUser(network, parsed["FromWhom"]).Roles:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Denied!\r\n")
			return
		
		if len(parsed["Arguments"]) < 4:
			network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Denied!\r\n")
			return
		
		self.voice.send_sms(parsed["Arguments"][2], parsed["RawArguments"][parsed["RawArguments"].find(parsed["Arguments"][2])+len(parsed["Arguments"][2])+1:])
	
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
		
		if self.voiceLoggedIn == False:
			self.voice.login()
			self.voiceLoggedIn = True
		
		network.Output.write("PRIVMSG " + parsed["ReplyTo"] + " :Access Granted!\r\n")
