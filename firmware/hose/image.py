#!/usr/bin/env python
print("Generating LittleFS image for WebVM")

from littlefs import LittleFS
from os import listdir, path

def traverse(root: str):
	files = listdir(root)
	outfiles = []
	outfolders = []

	for file in enumerate(files):
		files[file[0]] = "%s/%s" % (root, file[1])
		if path.isdir(files[file[0]]):
			outfolders.append(files[file[0]])
			trav = traverse(files[file[0]])
			outfiles.extend(trav[0])
			outfolders.extend(trav[1])
		else:
			outfiles.append(files[file[0]])
	
	return (outfiles, outfolders)

(files, folders) = traverse('build')
folders = list(map(lambda x: '/'.join(x.split('/')[1:]), folders))

print("Files found:")
for file in files:
	print(file)

output_img = 'hosefirmware.img'
lfs = LittleFS(block_size=4096, block_count=352, prog_size=256)

for folder in folders:
	print("Creating dir %s" % folder)
	lfs.mkdir(folder)

for file in files:
	lf_path = '/'.join(file.split('/')[1:])
	with open(file, 'rb') as f, lfs.open(lf_path, 'wb') as lf:
		print('Writing file %s to %s' % (file, lf_path))
		lf.write(f.read())

print('Saving img ' + output_img)
with open(output_img, 'wb') as fh:
	fh.write(lfs.context.buffer)