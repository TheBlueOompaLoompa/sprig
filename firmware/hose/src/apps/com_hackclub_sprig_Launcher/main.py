from ili9341 import color565
from app import App, ListMenu, ListMenuItem, list_apps
import json
import os

def setup():
	sprig = app.sprig
	sprig.fbuf.fill(color565(0, 0, 0))
	sprig.flip_buf()

	sprig.on_press('w', w)
	sprig.on_press('s', s)
	sprig.on_press('l', l)
	sprig.on_press('i', i)
	sprig.on_release('k', k_release)

	applist = []
	for a in list_apps():
		if not("hidden" in a and a['hidden']):
			applist.append(ListMenuItem(a['name'], activate=launch, extra=a))
	app.data['menu'] = ListMenu(sprig, ListMenuItem('', children=applist), 12, 128-12)

	draw()

def draw():
	sprig = app.sprig
	app.data['menu'].draw()
	if len(app.data['menu'].item.children) == 0:
		sprig.fbuf.text("No apps found!", 0, 12, color565(255, 255, 255))
	sprig.fbuf.text("Sprig Launcher", 0, 0, color565(0, 255, 0))
	sprig.flip_buf()

def w():
	app.data['menu'].up()
	draw()

def s():
	app.data['menu'].down()
	draw()

def l():
	app.system.quit()

def i():
	app.system.reset()

def k_release():
	app.data['menu'].activate()

def launch(item: ListMenuItem):
	app.system.launch(item.extra['appid'])

def loop():
	pass

app = App(setup, loop)
