# hose - Sprig MicroPython Firmware

This isn't being made as any sort of replacement or anything, just an alternative with the python ecosystem. The goal is to have a platform similar to spade with the same amount of hackability, but with MicroPython. This has the added bonus of being able to draw stuff directly if necessary, but by default the easy

## Requirements:
- Python 3 Installation
- [Nodemon](https://www.npmjs.com/package/nodemon) - For dev script
- Linux or MacOS(Maybe)
	- Will add Windows scripts if someone makes a pr for it
- A Sprig device

## Setup:
1. Put the sprig into bootloader mode by holding the BOOTSEL button while plugging it into your computer
2. Go to https://micropython.org/download/RPI_PICO_W/ and download the latest firmware uf2 (Not preview)
3. Upload the MicroPython uf2 and wait for it to reboot
4. Clone this repository and cd into it
5. Make dev.sh executable
	- *nix `chmod +x dev.sh`
6. Run the `dev.sh` script
7. End the script
8. Run `ampy put boot /`
9. Reboot the device and happy hacking!

## TODO:
- [x] Create basic setup with settings and launcher
- [ ] Add audio support
- ~~[ ] Add network support~~
- [ ] Add wired serial communication
- [ ] Graphics helpers
    - [ ] Tilemap
    - [ ] (Maybe if necessary) Custom MicroPython firmware with native draw functions and display driver
- Builtin Apps
	- [ ] Software gallery (when) if networking is added
	- [ ] Settings (Re-make for new architecture)
	- [ ] Getting Started (Finish)
	- [ ] Dev Tools (Re-make or remove)
