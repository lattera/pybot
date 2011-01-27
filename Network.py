import sys, time
from select import select
from socket import socket, AF_INET, SOCK_STREAM

from Bot import *
from Module import ModuleArgument

class Channel:
	def __init__(self, name=""):
		self.Name = name
		self.Active = False

class Network:
	def __init__(self, name, hostname, port, nick, channels=list(), connectNow=False):
		self.Name = name
		self.Hostname = hostname
		self.Port = port
		self.Nick = nick
		self.Channels = channels
		self.LastPingTime = 0
		self.Users = list()
		self.Socket = None
		self.Input = None
		self.Output = None
		if (connectNow):
			self.Connect()
	
	def Connect(self):
		self.Socket = socket(AF_INET, SOCK_STREAM)
		self.Socket.connect((self.Hostname, self.Port))
		self.Input = self.Socket.makefile('rb', 0)
		self.Output = self.Socket.makefile('wb', 0)
	
	def Identify(self):
		if self.Output == None:
			self.Connect()
		
		self.Output.write("NICK " + self.Nick + "\r\n")
		self.Output.write("USER " + self.Nick + " 8 * :" + self.Nick + "\r\n")
	
	def JoinChannel(self, channel):
		c = None
		for c in self.Channels:
			if c.Name == channel:
				break
		
		if c == None:
			self.Channels.append(Channel(channel))
			c = self.Channels[-1];
		
		if c.Active == False:
			self.Output.write("JOIN " + channel + "\r\n")
			c.Active = True
	
	def PartChannel(self, channel):
		for c in self.Channels:
			if c.Name == channel and c.Active == True:
				self.Output.write("PART " + channel + "\r\n")
				c.Active = False
	
	def Read(self, bot):
		data = self.Input.readline().strip()
		mainParts = data.split(":")
		serverInfo = mainParts[1].split(" ")
		
		serverInfo[1] = serverInfo[1].lower()
		if serverInfo[1] == "376":
			# Only join channels after MOTD
			self.CheckPing()
			for channel in self.Channels:
				self.Output.write("JOIN " + channel.Name + "\r\n")
				channel.Active = True
		else:
			for module in bot.modules:
				if serverInfo[1] in module.Commands:
					if module.NeedsBot:
						module.Queue.put(ModuleArgument(serverInfo[1], self, data, bot))
					else:
						module.Queue.put(ModuleArgument(serverInfo[1], self, data))
	
	def CheckPing(self):
		if time.time() - self.LastPingTime > 10:
			self.LastPingTime = time.time()
			realTime = repr(self.LastPingTime)
			if "." in realTime:
				realTime = realTime.split(".")[0]
			self.Output.write("PING :" + repr(realTime) + "\r\n")
	
	@staticmethod
	def InitializeNetworks(bot):
		for network in bot.networks:
			network.Connect()
			network.Identify()
	
	@staticmethod
	def RunLoop(bot):
		while True:
			readsocks = []
			for network in bot.networks:
				readsocks.append(network.Socket)
		
			readables, writeables, exceptions = select(readsocks, [], [], 10)
			for network in bot.networks:
				network.CheckPing()
				if network.Socket in readables:
					network.Read(bot)
