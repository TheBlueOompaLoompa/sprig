from ili9341 import color565
from app import App, list_apps
from machine import reset, UART
import os
import json
import gc
import sys

class System:
	def __init__(self):
		self.app: App = None
		self.apps = list_apps()
		self._queue = []
		self.settings = {
			"splash": True
		}
		self.uart = UART(0, 115200)
		self.uart.irq(UART.RX_ANY, handler=self._on_uart)

		self.load_settings()
		self.save_settings()

	def _on_uart(self):
		self.uart.write(self.uart.read())


	def load_settings(self):
		try:
			os.stat('/settings.json')
			with open('/settings.json') as f:
				data = json.load(f)
				for key in self.settings.keys():
					if key in data:
						self.settings[key] = data[key]
		except OSError:
			print("Settings file not found")

	def save_settings(self):
		with open('/settings.json', 'w') as f:
			json.dump(self.settings, f)
		print('Settings Saved')
		self.load_settings()

	def _loop(self):
		if self.app:
			self.app._loop()
		for action in self._queue:
			name = action[0]
			if name == 'launch':
				appid = action[1]
				print("Launching " + appid)
				if self.app != None:
					self.app.__deinit__()
					del sys.modules['apps.' + self.app.appid + '.main']
				del self.app
				gc.collect()
				for app in self.apps:
					if app['appid'] == appid:
						exec('import apps.' + appid + '.' + app['module'] + ' as sprigapp', {})
						self.app = sys.modules['apps.' + appid + '.main'].app
						self.app.appid = appid
						self.app.system = self
						self.app.setup()
			elif name == 'quit':
				return False
		self._queue.clear()
		return True

	def launch(self, appid: str):
		self._queue.append(['launch', appid])
	
	def quit(self):
		self._queue.append(['quit'])
	
	def reset(self):
		reset()
	
