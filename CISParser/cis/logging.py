# CIS module for logging info
from os.path import abspath
from datetime import datetime
from colorama import init
from termcolor import cprint, colored


def print_frame(header):
    """ Prints frames aroung decorated function """
    def decorator(decorated_func):
        def wrapper(*args, **kwargs):
            len_del = 100
            if header:
                lh = '-' * (len_del//2 - len(header)//2 - 1)
                msg = f"{lh} {header} {lh}"[:100]
                len_del = len(msg)
            else:
                msg = '-' * len_del
            logging._logging(msg)
            decorated_func(*args, **kwargs)
            logging._logging('-'*len_del)
        return wrapper
    return decorator

class logging(object):
    """ 
        Logging message to log file and stdout 
        ```
        @methods
        info, error, debug - levels of logging
        ```
    """
    debug_flag = False

    def __init__(self):
        init() # makes colors works in win cmd

    @classmethod
    def _logging(cls, msg, stdout=True, to_log=True, add_time=False):
        if stdout:
            print(msg)
        if to_log:
            with open('log.txt', 'a', encoding='utf-8') as log:
                if add_time:
                    msg = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
                print(msg, file=log)
    
    @print_frame('CISParser starts')
    def add_header(self, path, config, files_num, ver):
        self.files_num = files_num
        self.stime = datetime.now()
        self._logging(f"Version: {ver}")
        print(f"Launch mode: {colored('debug','yellow') if self.debug_flag else 'normal'}")
        self._logging(f"Launch mode: {'debug' if self.debug_flag else 'normal'}", stdout=False)
        self._logging(f"Start time: {self.stime:%Y-%m-%d %H:%M:%S}")
        if config:
            self._logging(f"Config file: {abspath('config.yaml')}")
        self._logging(f"Process path: {abspath(path)}")
        self._logging(f"Files to process: {files_num}")
    
    @print_frame(f'CISParser complied all tasks')
    def add_footnote(self):
        self.etime = datetime.now()
        delta = self.etime - self.stime
        self._logging(f"End time: {self.stime:%Y-%m-%d %H:%M:%S}")
        self._logging(f"Processing time: {(delta.seconds//60)%60}m {delta.seconds}s")
        self._logging(f"Processed files: {self.files_num}")

    @classmethod
    def info(cls, msg, to_log=True):
        print(f"{colored('INFO', 'magenta')}  : {msg}")
        cls._logging(f"INFO  : {msg}", stdout=False, to_log=to_log, add_time=True)

    @classmethod
    def error(cls, msg, to_log=True):
        print(f"{colored('ERROR', 'red')} : {msg}")
        cls._logging(f"ERROR : {msg}", stdout=False, to_log=to_log, add_time=True)

    @classmethod
    def debug(cls, msg, to_log=True):
        if not cls.debug_flag:
            return
        print(f"{colored('DEBUG', 'yellow')} : {msg}")
        cls._logging(f"DEBUG : {msg}", stdout=False, to_log=to_log, add_time=True)
