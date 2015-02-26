#!/usr/bin/env python
"""
This script runs a single pyulog unit test. It is called from the pyulog.py module when
run from __main__.

usage: unit_test.py -d directory_env -l line_to_log -m pyulog_mode_env -p user_prompt -s log_mask -v log_level
"""

import sys
import getopt
import os

def exit_with_usage():
	print(globals()['__doc__'])
	sys.exit(-1)

if __name__ == "__main__":

	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'd:l:m:p:s:v:', ['help','h','?'])
	except:
		import traceback
		traceback.print_exc()
		exit_with_usage()
	options = dict(optlist)
	if len(args) > 1:
		exit_with_usage()

	if [elem for elem in options if elem in ['-h','--h','-?','--?','--help']]:
		print("Help:")
		exit_with_usage()

	if '-d' in options:
		directory = options['-d']
	else:
		exit_with_usage()

	if '-l' in options:
		log_line = options['-l']
	else:
		exit_with_usage()

	if '-m' in options:
		mode = options['-m']
	else:
		exit_with_usage()

	if '-p' in options:
		prompt = options['-p']
	else:
		exit_with_usage()

	if '-s' in options:
		mask = options['-s']
	else:
		exit_with_usage()

	if '-v' in options:
		level = options['-v']
	else:
		exit_with_usage()

	if len(mode) > 0:
		os.environ['PYLOG_MODE'] = mode

	if len(directory) > 0:
		os.environ['PYLOG_DIR'] = directory

	import pyulog

	e_str = 'lev = pyulog.%s' % level
	exec(e_str)

	e_str = 'mas = pyulog.%s' % mask
	exec(e_str)

	pyulog.openlog('pyulog-unit-test', pyulog.LOG_PID, pyulog.LOG_DAEMON)
	pyulog.setlogmask(pyulog.LOG_UPTO(mas))

	pyulog.log(lev, log_line)
	ans = raw_input(prompt)
	if ans.lower() == 'y':
		pyulog.closelog()
		sys.exit(1)
	else:
		pyulog.closelog()
		sys.exit(0)

