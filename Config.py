from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from Network import *
from User import *

class Config(ContentHandler):
	def __init__(self, bot):
		self.isInNetwork = False
		self.isInBot = False
		self.isInAcl = False
		self.bot = bot
		self.channels = None
		self.user = None
		self.users = None
	
	def startElement(self, name, attrs):
		if name == "bot":
			self.isInBot = True
			self.ConfigVersion = attrs.get("version", "")
		elif name == "network":
			self.isInNetwork = True
			self.network = None
			self.networkname = attrs.get("name", "")
			self.channels = None
			self.users = None
		elif name == "net":
			self.hostname = attrs.get("hostname", "")
			self.port = attrs.get("port", "")
		elif name == "handle":
			self.nick = attrs.get("nick", "")
		elif name == "channel":
			if self.channels == None:
				self.channels = list()
			self.channels.append(Channel(attrs.get("name", "")))
		elif name == "acl":
			self.isInAcl = True
		elif name == "role":
			role = attrs.get("name", "")
			if role not in self.bot.acls:
				self.bot.acls.append(role)
		elif name == "user":
			if self.users == None:
				self.users = list()
			self.user = User(attrs.get("nick", ""), attrs.get("password", ""))
		elif name == "userrole":
			role = attrs.get("name", "")
			if role in self.bot.acls:
				self.user.Roles.append(role)
		
	def endElement(self, name):
		if name == "network":
			self.isInNetwork = False
			self.bot.networks.append(Network(self.networkname, self.hostname, int(self.port), self.nick, self.channels, False))
			for user in self.users:
				self.bot.networks[-1].Users.append(user)
		elif name == "acl":
			self.isInAcl = False
		elif name == "user":
			self.users.append(self.user)
