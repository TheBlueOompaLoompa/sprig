from ili9341 import color565
from app import App, ListMenu, ListMenuItem, list_apps, Sprig
import json
import os
import time
import math
from random import randint

last_time = 0
delay = 300

box_size = 10
margin = 1
x_cells = math.floor(160/box_size)
y_cells = math.floor(128/box_size)

snake = [(math.floor(x_cells/2), math.floor(y_cells/2))]
apple = (0, 0)
move_lock = False
move = (0, 0)

def place_apple():
	global apple
	apple_idx = randint(0, x_cells*y_cells-len(snake)-1)

	empty_found = False 

	while not(empty_found):
		x_cell = apple_idx % x_cells
		y_cell = math.floor(apple_idx / x_cells)
		empty_found = True
		for b in snake:
			if b == (x_cell, y_cell):
				empty_found = False

		if not(empty_found):
			apple_idx+=1
			if apple_idx >= x_cells*y_cells-1:
				apple_idx = 0
		else:
			apple = (x_cell, y_cell)


def setup():
	global snake
	global apple
	global move
	global move_lock
	sprig = app.sprig
	sprig.fbuf.fill(color565(0, 0, 0))
	sprig.flip_buf()

	snake = [(math.floor(x_cells/2), math.floor(y_cells/2))]
	place_apple()
	move = (1, 0)
	move_lock = False

	last_time = time.ticks_ms()
	delay = 1

	sprig.on_press('w', w)
	sprig.on_press('a', a)
	sprig.on_press('s', s)
	sprig.on_press('d', d)
	sprig.on_press('l', l)
	draw()

def box(sprig: Sprig, x_cell: int, y_cell: int, color: int = color565(255, 255, 255)):
	sprig.fbuf.fill_rect(x_cell*box_size+margin, y_cell*box_size+margin, box_size-margin*2, box_size-margin*2, color)

def draw():
	sprig = app.sprig
	sprig.fbuf.fill(color565(0, 0, 0))

	# Background
	for y in range(y_cells):
		for x in range(x_cells):
			box(sprig, x, y, color565(10, 10, 10))
	
	# Apple
	box(sprig, apple[0], apple[1], color565(255, 0, 0))

	# Snake
	for b in snake:
		box(sprig, b[0], b[1], color565(0, 255, 0))

	sprig.flip_buf()

def mov(x: int, y: int):
	global move
	global move_lock
	if not(move_lock) and (x, y) != move and (-x, -y) != move:
		move = (x, y)
		move_lock = True

def w():
	mov(0, -1)

def a():
	mov(-1, 0)

def s():
	mov(0, 1)

def d():
	mov(1, 0)

def l():
	app.quit()

def loop():
	global last_time
	global delay
	global snake
	global apple
	global move_lock
	global delay
	if delay <= time.ticks_ms() - last_time:
		last_time = time.ticks_ms()
		scored = False
		end_pos = (0, 0)

		for i in reversed(range(len(snake))):
			if i == 0:
				if len(snake) == 1:
					end_pos = snake[i]
				snake[i] = (snake[i][0]+move[0], snake[i][1]+move[1])
				if snake[i][0] >= x_cells:
					snake[i] = (0, snake[i][1])
				if snake[i][0] < 0:
					snake[i] = (x_cells-1, snake[i][1])
				if snake[i][1] >= y_cells:
					snake[i] = (snake[i][0], 0)
				if snake[i][1] < 0:
					snake[i] = (snake[i][0], y_cells-1)
				scored = snake[i] == apple
			else: 
				if len(snake) - 1 == i:
					end_pos = snake[i]
				snake[i] = (snake[i-1][0], snake[i-1][1])

		if scored:
			snake.append(end_pos)
			place_apple()

		for i in range(len(snake)):
			if i != 0 and snake[0] == snake[i]:
				app.quit()
		move_lock = False
		draw()

app = App(setup, loop)
