# Uses portions from i2s examples
# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

from sprig import Sprig
from machine import I2S, Pin
import struct
import math

class Audio:
	def __init__(self, sprig: Sprig):
		self.sample_rate = 24000
		self.bits = 16
		self.audio = I2S(0,
			sck=Pin(10), ws=Pin(11), sd=Pin(9),
			mode=I2S.TX,
			bits=self.bits,
			format=I2S.MONO,
			rate=self.sample_rate,
			ibuf=2000)
		self.tones: [Tone] = []
		self.audio.irq(self._audio_callback)
		self.sample_size_in_bytes = self.bits // 8

	def tone(self, wave: Wave, freq: float, length: float):
		"""Play a tone, length in seconds"""
		self.tones.append(Tone(wave, freq, length))

	def _audio_callback(self):
		for tone in tones:
			if tone.wave == Wave.SINE:
				self._sine(tone.freq)
	
	def _sine(self, frequency: float, time: float):
		# create a buffer containing the pure tone samples
		samples_per_cycle = int(self.sample_rate // frequency)
		samples = bytearray(samples_per_cycle * self.sample_size_in_bytes)
		volume_reduction_factor = 3
		int_range = pow(2, self.bits) // 2 // volume_reduction_factor
		
		format = "<h"
		
		for i in range(samples_per_cycle):
			sample = int_range + int(math.cos(math.tau * i / samples_per_cycle) * (int_range - 1))
			struct.pack_into('<h', samples, i * sample_size_in_bytes, sample)

		self.audio.write(samples)

	def triangle(self, freq: int, amp: float, length: float):
		real_length = length*self.sample_rate * 2
		buf = bytearray(real_length)
		for x in range(real_length):
			t = float(x) / float(freq)
			buf[x] = 4.0*abs(t/float(freq)-floor(t/float(freq)-0.5))-1.0

		self.audio.write(buf)

class Tone:
	def __init__(self, wave: Wave, freq: float, length: float):
		self.wave = wave
		self.freq = freq
		self.length = length

class Wave:
	SINE = 0
	TRIANGLE = 1
