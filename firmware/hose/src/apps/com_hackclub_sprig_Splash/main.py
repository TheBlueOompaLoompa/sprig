from ili9341 import color565
import framebuf
from app import App
from bmp_reader import BMPReader
import math
from time import sleep

def setup():
	sprig = app.sprig
	sprig.fbuf.fill(color565(0, 0, 0))
	sprig.flip_buf()
	steps = __file__.split('/')
	pathto = '/'.join(steps[0:len(steps)-1])
	splash = BMPReader(pathto + '/splash.bmp')

	splash_buf = framebuf.FrameBuffer(bytearray(160 * 128 * 2), 160, 128, framebuf.RGB565)
	for i in range(splash.width*splash.height):
		(pixel, x, y) = splash.read_pixel()
		splash_buf.pixel(x, y, pixel & 0xffff)

	offset = 0
	speed = 16
	while offset < 160 and offset > -200:
		sprig.fbuf.fill(0)
		sprig.fbuf.blit(splash_buf, offset, int(math.sin(float(offset)/30.0)*10.0))
		sprig.flip_buf()
		offset += speed
		speed -= 1
		sleep(0.01)

	del splash_buf
	app.quit()

def loop():
	pass

app = App(setup, loop)
