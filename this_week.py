#!/usr/bin/env python3
'''Publish one or more songs to this week folder

Usage:
  this_week.py <church> <song-prefix>...
  this_week.py <church> --clean

Arguments:
  <church>           name of church
  <song-prefix>      prefix of song name to publish

Options:
  --clean            clean out the specified church

Example:
  this_week.py 'Christ Church' 332
'''
import sys
import os
import glob

import docopt

script_dir = os.path.dirname(os.path.abspath(__file__))
ignored = ['.DS_Store', '.git', '.gitignore', '.idea', 'copyrights', 'tunes', 'content.json', 'this_week.py']


def copy_song_to_this_week(church, prefix, hymnal=''):
	hymnals_dir = os.path.join(script_dir, '..', 'hymnals', hymnal)
	this_week_dir = os.path.join(script_dir, church)
	if not os.path.exists(this_week_dir):
		os.makedirs(this_week_dir)
	found = False
	for hymnal_dir in os.listdir(hymnals_dir):
		hymnal_dir_path = os.path.join(hymnals_dir, hymnal_dir)
		if os.path.isdir(hymnal_dir_path):
			for filename in os.listdir(hymnal_dir_path):
				filename_path = os.path.join(hymnal_dir_path, filename)
				if (filename.startswith(prefix) or filename.startswith('_' + prefix)) and os.path.isfile(filename_path):
					found = True
					print('Copying ' + filename)
					song_number = 0
					for file in os.listdir(this_week_dir):
						if file not in ignored:
							song_number += 1
					song_letter = chr(ord('a') + song_number) + ' '
					this_week_song = os.path.join(this_week_dir, song_letter + filename.replace('_', ''))
					import_path = os.path.join('../..', 'hymnals', hymnal_dir, filename)
					with open(this_week_song, "w") as file:
						file.write('import ' + import_path + os.linesep)


	if not found:
		raise RuntimeError('Song not found with prefix "' + prefix + '"')

def main():
	arguments = docopt.docopt(__doc__)
	# church = arguments['<church>']
	# if not os.path.isdir(church):
	# 	raise RuntimeError('Church not found: ' + church)
	if arguments['--clean']:
		if arguments['<church>']:
			church_songs = os.path.join(script_dir, arguments['<church>'], '*')
		else:
			church_songs = os.path.join(script_dir, '*')
		for file in glob.glob(church_songs):
			if not file.endswith('py'):
				os.remove(file)
	else:
		for prefix in arguments['<song-prefix>']:
			copy_song_to_this_week(arguments['<church>'], prefix)


if __name__ == '__main__':
	main()
