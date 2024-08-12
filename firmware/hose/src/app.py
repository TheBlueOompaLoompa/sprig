from ili9341 import color565
from sprig import Sprig
import os
import json

class App:
	def __init__(self, setup, loop):
		self.setup = setup
		self.loop = loop
		self.data = {}
		self.sprig: Sprig = Sprig()
		self.appid = ''
		self.system = None
		self._onpress = { 'w': [], 'a': [], 's': [], 'd': [], 'i': [], 'j': [], 'k': [], 'l': []} 
		self._onrelease = { 'w': [], 'a': [], 's': [], 'd': [], 'i': [], 'j': [], 'k': [], 'l': []} 
		print('App initialized')
	
	def __deinit__(self):
		self.sprig.__deinit__()

	def _setup(self):
		self._onpress = { 'w': [], 'a': [], 's': [], 'd': [], 'i': [], 'j': [], 'k': [], 'l': []} 
		self._onrelease = { 'w': [], 'a': [], 's': [], 'd': [], 'i': [], 'j': [], 'k': [], 'l': []} 
		return self.setup()

	def _loop(self):
		self.sprig._input()
		return self.loop()

	def on_press(self, button: str, callback):
		self._onpress[button].append(callback)

	def on_release(self, button: str, callback):
		self._onrelease[button].append(callback)
	
	def quit(self):
		self.system.launch('com_hackclub_sprig_Launcher')

def list_apps():
	apps = []
	for app_dir in os.listdir('/apps'):
		try:
			manifest = open_manifest(app_dir)
			manifest['appid'] = app_dir
			apps.append(manifest)
			print('Found app ' + app_dir)
		except Exception:
			print('Error: Missing manifest - ' + app_dir)

	return apps

def open_manifest(appid):
	manifest = None
	os.stat('/apps/' + appid + '/manifest.json')
	with open('/apps/' + appid + '/manifest.json', 'rt') as manifest_file:
		manifest = json.loads(manifest_file.read())
	return manifest

class ListMenu:
	def __init__(self, sprig: Sprig, item: ListMenuItem, offset=0, height=128):
		self.path: [str] = []
		self.item = item
		self.sprig = sprig
		self.offset = offset
		self.height = height
		childs = []
		for x in item.children:
			childs.append(x.text)
		self.list = SelectorList(self.sprig, childs, offset + 12, height)
	
	def _find_path(self, path: [str], level: ListMenuItem):
		if len(path) == 0: return level

		for item in level.children:
			if item.text == path[0]:
				if len(path) > 0:
					return self._find_path(path[1:(len(path))], item)
				else:
					return item

	def draw(self):
		item = self._find_path(self.path, self.item)
		view = item.children
		self.list.draw()
		if len(view) == 0: return
		hovered_item = view[self.list.index]
		status_call = hovered_item.status
		if status_call != None:
			self.sprig.fbuf.text(status_call(hovered_item), 0, self.offset, color565(0, 0, 255))

	def activate(self):
		self.path.append(self.list.items[self.list.index])
		item = self._find_path(self.path, self.item)
		if item.activate == None:
			childs = []
			for x in item.children:
				childs.append(x.text)
			self.list = SelectorList(self.sprig, childs, self.offset + 12, self.height)
		else:
			self.path.pop()
			item.activate(item)

	def back(self):
		self.path.pop()
		childs = []
		for x in self._find_path(self.path, self.item).children:
			childs.append(x.text)
		self.list = SelectorList(self.sprig, childs, self.offset + 12, self.height)

	def up(self):
		self.list.up()

	def down(self):
		self.list.down()


class ListMenuItem:
	def __init__(self, text: str, status = None, activate = None, children: [ListMenuItem] = [], extra = None):
		self.status = status
		self.activate = activate
		self.children = children
		self.text = text
		self.extra = extra

class SelectorList:
	def __init__(self, sprig: Sprig, items: [str], y_pos = 0, height = 128):
		self.items = items
		self.index = 0
		self.offset = 0
		self.y_pos = y_pos
		self.height = height
		self.sprig = sprig

	def draw(self):
		vspacing = 12
		self.sprig.fbuf.fill(color565(0, 0, 0))
		for (row, text) in enumerate(self.items):
			if row == self.index:
				self.sprig.fbuf.rect(0, (self.index - self.offset) * vspacing + self.y_pos, 160, vspacing, color565(255, 255, 255), True)
			if row >= self.offset:
				self.sprig.fbuf.text(text, 0, (row - self.offset) * vspacing + int((vspacing-8)/2) + self.y_pos, color565(255, 255, 255) if row != self.index else color565(0, 0, 0))

	def up(self):
		self.index -= 1
		if self.index < 0:
			self.index = len(self.items) - 1

	def down(self):
		self.index += 1
		if self.index >= len(self.items):
			self.index = 0

class Keyboard:
	def __init__(self, sprig, layout):
		self.sprig = sprig
		self.layout = layout
		self.x = 0
		self.y = 0
		self.shift = 0
		self.visible = False
		self.buffer = ''
		self.title = 'Untitled'
		self._on_key = None

		sprig.on_press('w', self._w)
		sprig.on_press('s', self._s)
		sprig.on_press('a', self._a)
		sprig.on_press('d', self._d)
		sprig.on_press('k', self._k)

	def _w(self):
		if self.visible:
			self.y -= 1
			if self.y < 0: self.y = len(self.layout[0]) - 1
			self.x = min(len(self.layout[0][self.y]) - 1, self.x)
			self._draw()

	def _s(self):
		if self.visible:
			self.y += 1
			if self.y >= len(self.layout[0]): self.y = 0
			self.x = min(len(self.layout[0][self.y]) - 1, self.x)
			self._draw()

	def _a(self):
		if self.visible:
			self.x -= 1 
			if self.x < 0: self.x = len(self.layout[0][self.y]) - 1
			self._draw()

	def _d(self):
		if self.visible:
			self.x += 1
			if self.x >= len(self.layout[0][self.y]): self.x = 0
			self._draw()

	def _k(self):
		if not(self.visible): return
		key = self.layout[1 if self.shift > 0 else 0][self.y][self.x]
		
		if key == '\r':
			self.shift += 1
			if self.shift > 2:
				self.shift = 0
			self._draw()
			return
		elif key == '\t':
			self.buffer = self.buffer[0:max(len(self.buffer)-2, 0)]
		elif key == '\n':
			pass
		else:
			self.buffer += key

		if self.shift == 1:
			self.shift = 0
		self._on_key(key)
		
		self._draw()

	def set_visible(self, vis: bool):
		self.visible = vis
		if self.visible:
			self._draw()

	def _draw(self):
		if not(self.visible): return
		self.sprig.fbuf.fill(color565(0, 0, 0))
		vspace = 12
		hspace = 12
		self.sprig.fbuf.text(self.title, 0, 0, color565(90, 90, 90))
		self.sprig.fbuf.text(self.buffer, 0, vspace, color565(255, 255, 255))
		self.sprig.fbuf.line(len(self.buffer)*8, vspace*2 - 1, len(self.buffer)*8+8, vspace*2 - 1, color565(255, 255, 255))

		for (ry, row) in enumerate(self.layout[1 if self.shift > 0 else 0]):
			y = ry+2
			for (x, char) in enumerate(row):
				color = color565(127, 127, 127) if self.x != x or self.y != ry else color565(0, 255, 0)
				if char == '\r':
					self.sprig.fbuf.text('Shift', 0, y*vspace, color)
				elif char == ' ':
					self.sprig.fbuf.text('Space', 6*8, y*vspace, color)
				elif char == '\t':
					self.sprig.fbuf.text('<-', 12*8, y*vspace, color)
				elif char == '\n':
					self.sprig.fbuf.text('Enter', 15*8, y*vspace, color)
				else:
					self.sprig.fbuf.text(char, x*hspace, y*vspace, color)
		self.sprig.flip_buf()

	def on_key(self, callback):
		self._on_key = callback

	LAYOUTS = {
		'QWERTY': [
			['`1234567890-=','qwertyuiop{}\\',"asdfghjkl;'",'zxcvbnm,./','\r \t\n'],
			['~!@#$%^&*()_+','QWERTYUIOP{}|','ASDFGHJKL:"','ZXCVBNM<>?','\r \t\n']
		],
		'WORKMAN': [
			['`1234567890-=','qdrwbjfup;[]\\',"ashtgyneoi'",'zxmcvkl,./','\r \t\n'],
			['~!@#$%^&*()_+','QDRWBJFUP:{}|','ASHTGYNEOI"','ZXMCVKL<>?','\r \t\n']
		]
	}
