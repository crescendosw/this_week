#!/usr/bin/env python3
'''Publish one or more songs to this week folder

Usage:
  this_week.py <song-prefix>...
  this_week.py --clean

Arguments:
  <song-prefix>      prefix of song name to publish

Options:
  --clean            clean out the specified church

Example:
  this_week.py 332
'''
import sys
import os
import glob

import docopt

script_dir = os.path.dirname(os.path.abspath(__file__))


def copy_song_to_this_week(church, prefix):
	hymnals_dir = os.path.join(script_dir, '..', 'hymnals')
	# this_week_dir = os.path.join(script_dir, church)
	this_week_dir = script_dir
	if not os.path.exists(this_week_dir):
		os.makedirs(this_week_dir)
	found = False
	for hymnal_dir in os.listdir(hymnals_dir):
		hymnal_dir_path = os.path.join(hymnals_dir, hymnal_dir)
		if os.path.isdir(hymnal_dir_path):
			for filename in os.listdir(hymnal_dir_path):
				filename_path = os.path.join(hymnal_dir_path, filename)
				if filename.startswith(prefix) and os.path.isfile(filename_path):
					found = True
					print('Copying ' + filename)
					this_week_song = os.path.join(this_week_dir, filename)
					import_path = os.path.join('..', 'hymnals', hymnal_dir, filename)
					with open(this_week_song, "w") as file:
						file.write('import ' + import_path + os.linesep)


	if not found:
		raise RuntimeError('Song not found with prefix "' + prefix + '"')

def main():
	arguments = docopt.docopt(__doc__)
	# church = arguments['<church>']
	# if not os.path.isdir(church):
	# 	raise RuntimeError('Church not found: ' + church)
	church = ''
	if arguments['--clean']:
		# church_songs = os.path.join(script_dir, church, '*')
		church_songs = os.path.join(script_dir, '*')
		for file in glob.glob(church_songs):
			if not file.endswith('py'):
				os.remove(file)
	else:
		for prefix in arguments['<song-prefix>']:
			copy_song_to_this_week(church, prefix)


if __name__ == '__main__':
	main()
