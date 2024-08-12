from ili9341 import color565
from app import App, list_apps
import os
import json
import gc

class System:
	def __init__(self):
		self.app: App = None
		self.apps = list_apps()
		self.settings = {
			"splash": False
		}

	def load_settings(self):
		try:
			os.stat('settings.json')
			with open('settings.json', 'rt') as settings_file:
				data = json.loads(settings_file.read())
				for key in settings.keys():
					if key in data:
						self.settings[key] = data[key]
		except Exception:
			print("Settings file not found")

	def save_settings(self):
		with open('settings.json', 'wt') as settings_file:
			settings_file.write(json.dumps(self.settings))

	def launch(self, appid: str):
		print("Launching " + appid)
		if self.app != None: self.app.__deinit__()
		del self.app
		gc.collect()
		for app in self.apps:
			if app['appid'] == appid:
				self.app = __import__('/apps/' + appid + '/' + app['module']).app
				self.app._system = self
				self.app.setup()
	
