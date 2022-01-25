from core import co_definitions
from core.mks import mks_config
import webview

class TerminalLayer(co_definitions.ILayer):
	def __init__(self):
		co_definitions.ILayer.__init__(self)
		self.ApplicationName 	= "Application"
		self.Application    	= None
		self.ProcessRunning 	= True
		self.Handlers 			= None
		self.Config 			= mks_config.NodeConfig()
		self.Handlers       	= {
			"help":         self.HelpHandler,
			"app":			self.AppHandler,
			"exit":			self.ExitHandler,
		}
	
	def UpdateApplication(self, data):
		if self.Application is not None:
			self.Application.EmitEvent(data)
	
	def HelpHandler(self, data):
		pass

	def ExitHandler(self, data):
		self.Exit()
	
	def AppHandler(self, data):
		# Generate command
		#cmd = '"c:\program files (x86)\Google\Chrome\Application\chrome.exe" --window-size=1400,800 -incognito --app="http://{0}:{1}"'.format(str(self.Config.Application["server"]["address"]["ip"]), str(self.Config.Application["server"]["web"]["port"]))
		#objFile = co_file.File()
		#objFile.Save("ui.cmd", cmd)
		#subprocess.call(["ui.cmd"])

		path = "http://{0}:{1}".format(str(self.Config.Application["server"]["address"]["ip"]), str(self.Config.Application["server"]["web"]["port"]))
		webview.create_window(self.ApplicationName, path)
		webview.start()
	
	def Run(self):
		status = self.Config.Load()
		if status is False:
			print("ERROR - Wrong configuration format")
			return False
		while(self.ProcessRunning is True):
			try:
				raw  	= input('> ')
				data 	= raw.split(" ")
				cmd  	= data[0]
				params 	= data[1:]

				if self.Handlers is not None:
					if cmd in self.Handlers:
						self.Handlers[cmd](params)
					else:
						if cmd not in [""]:
							print("unknown command")
			except Exception as e:
				print("Terminal Exception {0}".format(str(e)))
		return True
	
	def Exit(self):
		self.ProcessRunning = False
