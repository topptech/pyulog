# pyulog
Python unified logging interface module

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

Tested running Python 2.7 on 'linux2' and 'win32' platforms (sys.platform).

To install run:
    python setup.py install
        or
    sudo python setup.py install
