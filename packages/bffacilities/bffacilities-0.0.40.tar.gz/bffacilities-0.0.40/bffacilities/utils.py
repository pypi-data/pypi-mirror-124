
import platform
import os
import atexit
import logging
from pathlib import Path

__version__ = "0.1.1"

_LOG_DIR = Path.home() / ".bfp" / ".logs"   # Log Path
_LOG_DIR.mkdir(parents=True, exist_ok=True)

formaterStr = "%(asctime)s %(levelname)s:  %(message)s"

def createLogger(name: str, savefile = True, stream = False, 
    level = logging.INFO, basedir = None,  **kwargs):
    """create logger
    Args: 
        name : suffix will be appended, for example, `test` will be `test.log`
        basedir: default is `~/.logs`

    kwargs:
        timeformat: default is "%Y-%m-%d %H:%M:%S" 
    :: logger_prefix deprecated ::

    """

    logger = logging.getLogger(name)
    # print("create logger", name)
    # import traceback
    # traceback.print_stack()
    if hasattr(logger, "_bf_inited"):
        # return created logger
        # print("Created Logger Returned")
        return logger

    logger._bf_inited = True

    _formater = logging.Formatter(formaterStr, kwargs.get("timeformat", "%Y-%m-%d %H:%M:%S"))

    logger.setLevel(level)
    if savefile:
        if basedir is None:
            basedir = _LOG_DIR
        elif type(basedir) == str:
            basedir = Path(basedir)
        os.makedirs(basedir, exist_ok=True)
        if not name.endswith(".log"):
            name = name + ".log"
        log_file = basedir / name
        fh = logging.FileHandler(log_file)
        fh.setFormatter(_formater)
        fh.setLevel(level)
        logger.addHandler(fh)
        # print("add file handler", log_file)
    if stream:
        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(_formater)
        logger.addHandler(sh)
    return logger

def changeLoggerLevel(logger, level):
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

## ********** For Translating **************
_LANGUAGE_DIR = (Path(__file__).parent / "locale").resolve()
import gettext
def initGetText(domain="myfacilities", dirs = _LANGUAGE_DIR) -> gettext.gettext:
    """make some configurations on gettext module 
    for convenient internationalization
    """
    gettext.bindtextdomain(domain, dirs)
    gettext.textdomain(domain)
    gettext.find(domain, "locale", languages=["zh_CN", "en_US"])
    return gettext.gettext
## ********** For Translating **************

def lockfile(fileName, start = None, stop = None, logger=None):
    """
    original : Fix Multiple instances of scheduler problem  
        https://github.com/viniciuschiele/flask-apscheduler/issues/51
    :param str filename: specified lock filename, such as app.lock
    :param function start: callback for app loop start
    :param function stop: callback for app loop stop
    :@Return True success
    """
    if logger is None:
        logger = logging.getLogger("bffacilities")
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open(fileName, "wb")
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if start is not None:
                start()
            # logger.debug("Scheduler Started...")
        except Exception as e:
            logger.error('Exit the scheduler, error - {}'.format(e))
            if stop is not None:
                stop()
            return False
        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()
        atexit.register(unlock)
    else:
        msvcrt = __import__("msvcrt")
        f = open(fileName, "wb")
        logger.info("Lock file is: ", os.path.realpath(f.name))
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            if start is not None:
                start()
            # logger.debug("Scheduler Started...")
        except Exception as e:
            logger.error('Exit the scheduler, error - {}'.format(e))
            if stop is not None:
                stop()
            return False
        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                f.close()
                os.remove(f.name)
            except IOError:
                raise
        atexit.register(_unlock_file)
    return True

import hashlib
def simplePasswordEncry(password):
    t = hashlib.sha256(password.encode())
    d = t.digest()
    return ''.join(('{:02x}'.format(x) for x in d))

import subprocess
from ._constants import BFF_OTHER_PATH
def createShortCut(target, link = None, desc="", workingdir=None, desktop=None, startup=None):
    """target: Path
    """
    scriptPath = BFF_OTHER_PATH / "winbat" / "createshortcut.js"
    assert link is not None or desktop is not None or startup is not None
    if workingdir is None:
        assert isinstance(target, Path)
        workingdir = (target / "..").resolve()
    script = ["wscript.exe", str(scriptPath), 
        "--workingdir", str(workingdir),
        "--target", str(target),
        "--desc", desc,
        ]
    if desktop is not None:
        script.append("--desktop")
        script.append(desktop)
    if startup is not None:
        script.append("--startup")
        script.append(startup)

    try:
        process = subprocess.Popen(script, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # ret = p.stdout.read().decode()
    except Exception as e:
        logger = logging.getLogger("bffacilities")
        logger.warn(f"Error when creating shortcut {e} for {script}")
