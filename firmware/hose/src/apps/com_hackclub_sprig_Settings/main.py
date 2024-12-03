from ili9341 import color565
from app import App, SelectorList, ListMenu, ListMenuItem
from sprig import Sprig
import json
import os
import machine
import audio

def setup():
	sprig = app.sprig
	app.data['menu'] = ListMenu(
		sprig,
		ListMenuItem('', children=[
			ListMenuItem('Enter Bootloader', activate=bootloader),
			ListMenuItem('Toggle Splash', activate=splash, status=splash_status),
		]),
		offset=12,
		height=128-12
	)
	app.data['visible'] = True

	sprig.on_press('w', w)
	sprig.on_press('s', s)
	sprig.on_press('k', k)
	sprig.on_release('l', l)

	app.system.load_settings()

	aud = audio.Audio(sprig)
	aud.tone(audio.Wave.SINE, 440, 1)

	draw()

def bootloader(_item: ListMenuItem):
	machine.bootloader()

def splash(_item: ListMenuItem):
	app.system.settings['splash'] = not(app.system.settings['splash'])
	app.system.save_settings()

def splash_status(_item: ListMenuItem):
	return 'Splash is ' + ('Enabled' if app.system.settings['splash'] else 'Disabled')

def draw():
	if not(app.data['visible']): return
	app.sprig.fbuf.fill(0)
	app.data['menu'].draw()
	app.sprig.fbuf.text('Settings', 0, 0, color565(255, 0, 255))
	app.sprig.flip_buf()

def w():
	if not(app.data['visible']): return
	app.data['menu'].up()
	draw()

def s():
	if not(app.data['visible']): return
	app.data['menu'].down()
	draw()

def k():
	if not(app.data['visible']): return
	app.data['menu'].activate()
	draw()

def l():
	if not(app.data['visible']): return
	if len(app.data['menu'].path) == 0:
		app.quit()
	else:
		app.data['menu'].back()
		draw()

def loop():
	pass

app = App(setup, loop)
