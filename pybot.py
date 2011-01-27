#!/usr/bin/env python2.6

import os
import Queue
import signal
from xml.sax import make_parser

from Module import *
from Network import *
from Bot import *
from Config import *

bot = Bot()

def onSignal(signum, stackframe):
	Module.BroadcastEvent(bot, "die", None)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, onSignal)
	
	config = Config(bot)
	parser = make_parser()
	parser.setContentHandler(config)
	parser.parse(open('config.xml')) 
	
	bot.modules = Module.InitializeModules("modules")
	Network.InitializeNetworks(bot)
	
	Network.RunLoop(bot)
