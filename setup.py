
from distutils.core import setup
setup(name='utilities',
      version='1.0',
      description='Python logging utility',
      author='Wayne Topp',
      author_email='topptech at comcast dot net',
      license='Python Software Foundation License',
      py_modules=['pyulog'],
      long_description="""
      Python Logging Utility
      
      The pyulog module provides a platform independent syslog logging
      interface. It uses the Python logging module to provide an interface
      similar to syslog for platforms that do not provide syslog. Or it
      can be configured to use syslog on platforms that do provide syslog.
      The configuration is set using environment variables.
      """
      )
