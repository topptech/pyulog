"""
	This module provides a unified logging interface. It provides a syslog API
	even when the Python syslog module is not supported.

	When the syslog Python module is available, it is used unless configured to
	log to the console. Console logging is done through the Python logging
	module.

	When the syslog Python module is not available, the logging module
	is used to emulate the structure of a syslog message. In this mode,
	the message can be logged to the console or to a file.

	The mode of operation is configured through environment variables set by
	the user.

	Unix operation (any OS that supports the Python syslog module):
		The log is output to syslog by default. Set environment variable(s)
		to change the mode of operation:
			PYLOG_MODE unset   -> syslog used if available
			PYLOG_MODE=SYSLOG  -> syslog used
			PYLOG_MODE=CONSOLE -> log to stdout
			PYLOG_MODE=FILE    -> log to 'ident'.log file in current direectory
			PYLOG_DIR=         -> optional directory to create 'ident'.log file
		If syslog is not available or if PYLOG_MODE is set to something other than
		'SYSLOG' or 'CONSOLE' then logging will be to a file named 'ident'.log.
		Additionally, PYLOG_DIR can be set to a directory to store the log file.

	Windows operation:
		The log is output to the console by default. Configure as follows:
			PYLOG_MODE unset   -> log to stdout
			PYLOG_MODE=CONSOLE -> log to stdout
			PYLOG_MODE=FILE    -> log to 'ident'.log file in current directory
			PYLOG_DIR=         -> optional directory to create 'ident'.log file

	Note: PYLOG_MODE must be set before importing the pyulog module if the
	      default behavior is not desired. Once the module is imported the
	      mode of operation cannot be changed.
"""

import os

try:
	__pylog_mode = None
	try:
		__pylog_mode = os.environ['PYLOG_MODE']
	except:
		if __pylog_mode == None:
			pass

	if __pylog_mode != None and __pylog_mode.lower() != 'syslog':
			raise RuntimeError('Using logging module')

	import syslog
	LOG_PID = syslog.LOG_PID
	LOG_DAEMON = syslog.LOG_DAEMON
	openlog = syslog.openlog
	closelog = syslog.closelog
	setlogmask = syslog.setlogmask
	LOG_CRIT = syslog.LOG_CRIT
	LOG_ERR = syslog.LOG_ERR
	LOG_WARNING = syslog.LOG_WARNING
	LOG_INFO = syslog.LOG_INFO
	LOG_DEBUG = syslog.LOG_DEBUG
	LOG_UPTO = syslog.LOG_UPTO
	LOG_MASK = syslog.LOG_MASK

	def pyulog(priority, message):
		syslog.syslog(priority, message)

	log = pyulog

except:

	import logging
	import os.path
	import sys

	LOG_PID = None
	LOG_DAEMON = None

	LOG_CRIT = logging.CRITICAL
	LOG_ERR = logging.ERROR
	LOG_WARNING = logging.WARNING
	LOG_INFO = logging.INFO
	LOG_DEBUG = logging.DEBUG

	gident = os.path.basename(sys.argv[0])

	def openlog(ident=None, logopt=None, facility=None):
		global gident
		if ident != None:
			gident = ident

		stdout = False
		try:
			__pylog_mode = os.environ['PYLOG_MODE']
			if __pylog_mode.lower() == 'console':
				stdout = True
		except:
			stdout = True

		if stdout == False:
			try:
				sfilename = '%s%s%s.log' % (os.environ['PYLOG_DIR'], os.sep, gident)
			except:
				sfilename = '%s.log' % gident

			logging.basicConfig(filename=sfilename, filemode='a',
								format='%(asctime)s: [' + gident + ']: %(levelname)s: %(message)s',
								level=logging.DEBUG)
		else:
			logging.basicConfig(format='%(asctime)s: [' + gident + ']: %(levelname)s: %(message)s',
								handlers=[logging.StreamHandler()],
								level=logging.DEBUG)
		root_logger = logging.getLogger()
		root_logger.disabled = False


	def pyulog(priority, message):

		if priority == LOG_CRIT:
			logging.critical(message)
		elif priority == LOG_ERR:
			logging.error(message)
		elif priority == LOG_WARNING:
			logging.warning(message)
		elif priority == LOG_INFO:
			logging.info(message)
		else:
			logging.debug(message)


	log = pyulog


	def setlogmask(level):
		logging.root.setLevel(level)


	def LOG_UPTO(level):
		return level


	def LOG_MASK(level):
		return level


	def closelog():
		root_logger = logging.getLogger()
		root_logger.disabled = True
		logging.shutdown()


# Unit tests
if __name__ == "__main__":

	import subprocess
	import os
	import sys

	if os.environ.has_key('PYLOG_MODE') or os.environ.has_key('PYLOG_DIR'):
		print 'PYLOG_MODE and PYLOG_DIR must be unset before running the unit test.'
		sys.exit(1)
		
	syslog_support = True
	try:
		import syslog
	except:
		syslog_support = False

	if syslog_support:
		ques = 'in appropriate syslog file'
	else:
		ques = 'logged on the console'

	status = subprocess.call('.%sunit_test.py -d "" -l "Unit test 1." -m "" -p "Was line (Unit test 1.) %s? [y/n] " -s LOG_DEBUG -v LOG_DEBUG' % (os.sep, ques), shell=True)
	if status != 1:
		print 'Unit test 1 failed!'
		sys.exit(1)

	status = subprocess.call('.%sunit_test.py -d "" -l "Unit test 2." -m "" -p "Was line (Unit test 2.) %s? [y/n] " -s LOG_INFO -v LOG_DEBUG' % (os.sep, ques), shell=True)
	if status != 0:
		print 'Unit test 2 failed!'
		sys.exit(1)
	else:
		status = 1

	status = subprocess.call('.%sunit_test.py -d "" -l "Unit test 3." -m "FILE" -p "Was line (Unit test 3.) in pyulog-unit-test.log file? [y/n] " -s LOG_INFO -v LOG_INFO' % os.sep, shell=True)
	if status != 1:
		print 'Unit test 3 failed!'
		sys.exit(1)

	status = subprocess.call('.%sunit_test.py -d "" -l "Unit test 4." -m "FILE" -p "Was line (Unit test 4.) in pyulog-unit-test.log file? [y/n] " -s LOG_WARNING -v LOG_INFO' % os.sep, shell=True)
	if status != 0:
		print 'Unit test 4 failed!'
		sys.exit(1)
	else:
		status = 1

	status = subprocess.call('.%sunit_test.py -d "%stmp" -l "Unit test 5." -m "FILE" -p "Was line (Unit test 5.) in %stmp%spyulog-unit-test.log file? [y/n] " -s LOG_WARNING -v LOG_WARNING' % (os.sep, os.sep, os.sep, os.sep), shell=True)
	if status != 1:
		print 'Unit test 5 failed!'
		sys.exit(1)

	status = subprocess.call('.%sunit_test.py -d "%stmp" -l "Unit test 6." -m "FILE" -p "Was line (Unit test 6.) in %stmp%spyulog-unit-test.log file? [y/n] " -s LOG_ERR -v LOG_WARNING' % (os.sep, os.sep, os.sep, os.sep), shell=True)
	if status != 0:
		print 'Unit test 6 failed!'
		sys.exit(1)
	else:
		status = 1

	status = subprocess.call('.%sunit_test.py -d "" -l "Unit test 7." -m "CONSOLE" -p "Was line (Unit test 7.) logged on the console? [y/n] " -s LOG_ERR -v LOG_ERR' % os.sep, shell=True)
	if status != 1:
		print 'Unit test 7 failed!'
		sys.exit(1)

	status = subprocess.call('.%sunit_test.py -d "" -l "Unit test 8." -m "CONSOLE" -p "Was line (Unit test 8.) logged on the console? [y/n] " -s LOG_CRIT -v LOG_ERR' % os.sep, shell=True)
	if status != 0:
		print 'Unit test 8 failed!'
		sys.exit(1)
	else:
		status = 1

	status = subprocess.call('.%sunit_test.py -d "" -l "Unit test 9." -m "CONSOLE" -p "Was line (Unit test 9.) logged on the console? [y/n] " -s LOG_CRIT -v LOG_CRIT' % os.sep, shell=True)
	if status != 1:
		print 'Unit test 8 failed!'
		sys.exit(1)

	if status == 1:
		print 'Unit tests passed!'

