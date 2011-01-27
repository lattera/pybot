class User:
	def __init__(self, username="", password=""):
		self.Username = username
		self.Password = password
		self.Roles = list()

class Authentication:
	def __init__(self):
		self.DataStore = dict()
	
	def GetUser(self, network, username):
		anon = None
		user = None
		for u in network.Users:
			if u.Username == username:
				user = u
				break
			elif u.Username == "*":
				anon = u
		
		if user == None:
			return anon
		
		return user
	
	def GetAuthenticatedUser(self, network, username):
		anon = None
		user = None
		for u in network.Users:
			if u.Username == username:
				user = u
			elif u.Username == "*":
				anon = u
		
		if user == None:
			return anon
		if not network.Name in self.DataStore:
			return anon
		if not username in self.DataStore[network.Name]:
			return anon
		if self.DataStore[network.Name][username]["Authenticated"] == False:
			return anon
		
		return user
	
	def IsAuthenticated(self, network, username):
		user = self.GetUser(network, username)
		if user.Username == "*":
			return True
		
		if not network.Name in self.DataStore:
			return False
		if not username in self.DataStore[network.Name]:
			return False
		
		return self.DataStore[network.Name][username]["Authenticated"]
	
	def NeedsAuthentication(self, network, username):
		user = self.GetUser(network, username)
		if user.Username == "*":
			return False
		
		return True
	
	def GetRoles(self, network, username):
		user = self.GetUser(network, username)
		return user.Roles
	
	def AuthenticateUser(self, network, username, password):
		if self.NeedsAuthentication(network, username) == False:
			return True
		
		user = self.GetUser(network, username)
		if user.Password != password:
			return False
		
		if not network.Name in self.DataStore:
			self.DataStore[network.Name] = dict()
		if not username in self.DataStore[network.Name]:
			self.DataStore[network.Name][username] = dict()
		
		self.DataStore[network.Name][username]["Authenticated"] = True
		
		return True
		
	def DeauthenticateUser(self, network, username):
		if self.NeedsAuthentication(network, username) == False:
			return
		if self.IsAuthenticated(network, username) == False:
			return
		self.DataStore[network.Name][username]["Authenticated"] = False
