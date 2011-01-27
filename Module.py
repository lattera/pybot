# -*- coding: utf-8 -*-
import os
import threading
import Queue

class ModuleArgument:
	def __init__(self, name, arg=None, data="", auxData=None):
		self.Name = name
		self.Arg = arg
		self.Data = data
		self.AuxData = auxData

class Module:
	def __init__(self):
		self.ModuleName = ""
		self.module = None
		self.Instance = None
		self.Active = True
		self.ThreadSpun = False
		self.Queue = Queue.Queue(0)
		self.NeedsBot = False
		self.Commands = list()
	
	@staticmethod
	def InitializeModules(directory):
		modules = list();
		for mod in os.listdir(directory):
			if mod != "__init__.py" and mod[-3:] != "pyc" and mod[0] != ".":
				module = Module()
				module.ModuleName = mod[0:-3]
				print "Adding: " + module.ModuleName
				module.module = __import__("modules." + module.ModuleName, globals(), locals(), module.ModuleName, -1)
				exec("module.Instance = module.module." + module.ModuleName + "(module.Queue)")
				module.Instance.start()
				module.ThreadSpun = True
				modules.append(module)
				module.Queue.put(ModuleArgument("Initialize", module))
				
		return modules
	
	@staticmethod
	def BroadcastEvent(bot, name, arg):
		for module in bot.modules:
			module.Queue.put(ModuleArgument(name, arg))

class IModule (threading.Thread):
	def GetParts(self, data):
		mainParts = data.strip().split(":")
		serverParts = mainParts[1].strip().split(" ")
		fromwhom = mainParts[1].split("!")[0]
		towhom = serverParts[2].strip()
		line = data[data.find(towhom)+len(towhom)+2:].strip()
		arguments = line.split(" ")
		
		retval = dict()
		retval["FromWhom"] = fromwhom
		retval["ToWhom"] = towhom
		retval["Arguments"] = arguments
		retval["RawArguments"] = line
		if towhom[0] == "#":
			retval["ReplyTo"] = towhom
		else:
			retval["ReplyTo"] = fromwhom
		
		return retval
		
	def __init__(self):
		if self.__class__ is IModule:
			raise NotImplementedError
	
	def run(self):
		if self.__class__ is IModule:
			raise NotImplementedError
