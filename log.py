"""
Basic logging tools
"""
import logging
import settings
from logging.handlers import RotatingFileHandler
import sys
import os

logger = logging.getLogger(settings.LOG_NAME)
logger.setLevel(settings.LOG_LEVEL)
#fh = logging.FileHandler(settings.LOG_FILE)
#fh.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s]: %(message)s"))
#fh.setLevel(settings.LOG_LEVEL)
#logger.addHandler(fh)



log_formatter = logging.Formatter('%(asctime)-10s %(levelname)-8s %(module)s %(funcName)s(%(lineno)d) %(message)s')
log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"
logFile = settings.LOG_FILE

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(settings.LOG_LEVEL)


logger.addHandler(my_handler)

if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

# next bit filched from 1.5.2's inspect.py
def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back

if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(3)



def debug(msg):
    """ Logs a debug message to the logger """
    if logger.level <= logging.DEBUG:
        print('\n~ ' + msg)
    logger.debug(msg)


def info(msg):
    """ Logs an info message to the logger """
    if logger.level <= logging.INFO:
        print('\n~ ' + msg)
    logger.info(msg)


def error(msg):
    """ Logs an error message to the logger """
    if logger.level <= logging.ERROR:
        print('\n~ ' + msg)
    logger.info(msg)


#_srcfile = os.path.normcase(currentframe.__code__.co_filename)

def findCallerPatch():
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = currentframe()
    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        rv = (filename, f.f_lineno, co.co_name)
        break
    return rv

# DO patch
logger.findCaller = findCallerPatch