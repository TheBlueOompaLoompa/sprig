import gc
from system import System

system = System()
if system.settings['splash']:
	system.launch('com_hackclub_sprig_Splash')
else:
	system.launch('com_hackclub_sprig_Launcher')

while system._loop() == True:
	pass
