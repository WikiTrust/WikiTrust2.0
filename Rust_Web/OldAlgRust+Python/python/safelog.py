#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 Camiolog Inc.
# Authors: Luca de Alfaro and Massimo Di Pierro
# License: BSD

import os
import csv
import datetime
import inspect
import traceback
import re
import threading
import logging
from functools import wraps

MAX_BYTES = 5*1024 # max number of bytes of logfile reported to server
jpeg = re.compile('''['"]\/9j\/.*?['"]''')
LOG_LEVELS = {'debug':10, 'info':20, 'warning':30, 'warn':30, 'error':40, 'critical':50}

try:
    from google.appengine.ext import db as gae
    IS_GAE = True
except ImportError:
    from fcntl import flock, LOCK_EX, LOCK_UN
    IS_GAE = False

class SmartLogger(object):

    def __init__(self, filename, level=20, console=True,
                 maxsize=1e7, truncate=4e4, url=None,
                 callback=None):
        self.filename = filename
        self.lock_filename = filename+'.lock'
        self.maxsize = maxsize
        self.truncate = truncate and int(truncate)
        self.level = level
        self.console = console
        self.callback = callback

    def set_level(self, level):
        self.level = level

    def get_log_data(self, name, message, use_introspection):
        message = jpeg.sub("'[JPEG DATA]'", message)
        message = message.strip()
        dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')[:23]
        pid = os.getpid()
        level = name.upper()
        thread = threading.currentThread().ident
        data = dict(datetime=dt, pid=pid, level=level, thread=thread, message=message, module='', function='', lineno='')
        if use_introspection:
            calframe = inspect.getouterframes(inspect.currentframe())
            data.update(
                module=calframe[3][1].lstrip('./'),
                lineno=calframe[3][2],
                function=calframe[3][3])
        data['escaped_message'] = message.replace('"', '""')
        # print data
        return data

    def writelog(self, name, text, args=None):
        try:
            level = LOG_LEVELS.get(name, 0)
            message = text
            if args:
                if len(args) == 1:
                    args = args[0]
                message = text % args
        except Exception as e:
            message = 'Internal Logging Error: %s' % e

        # if we are on GAE use the build-in logger
        if IS_GAE:
            getattr(logging, name)(message)
            return

        # if we aren't going to log it don't bother constructing the log string
        if level < self.level:
            return

        use_introspection = True
        # use introspection on error to help with debugging
        if level >= LOG_LEVELS.get('error', 0):
            use_introspection = True

        # do not show jpeg strings
        data = self.get_log_data(name, message, use_introspection)
        logline = '{datetime},{level},{pid},{thread},{module},{function},{lineno},"{escaped_message}"'.format(**data)

        if level >= self.level:
            locker = open(self.lock_filename,'wb')
            locked = False
            try:
                try:
                    flock(locker, LOCK_EX)
                    locked = True
                except Exception as e:
                    if self.console:
                        print('>>> Unable to lock: %s' % e)
                else:
                    if self.truncate:
                        self.truncate_file(bytes = len(logline))
                    with open(self.filename, 'ab') as myfile:
                        myfile.write(logline+'\n')
                if self.console:
                    print(logline)
            except:
                if self.console:
                    print(traceback.format_exc())
            finally:
                if locked:
                    flock(locker, LOCK_UN)
            if self.callback:
                try:
                    code = "{module}:{function}:{lineno}".format(**data)
                    self.callback(name, code, logline, logger=self)
                except:
                    pass


    def truncate_file(self, bytes):
        """ alternative to log rotation, the same file is shortened to make space """
        try:
            size = os.path.getsize(self.filename)
        except OSError:
            return
        else:
            if size+bytes > self.maxsize:
                with open(self.filename, 'rb') as myfile:
                    # find all lines that name a task define as (pid,thread)
                    rows = [row for row in csv.reader(myfile)]
                    counter = 0
                    data = ''
                    tasks = set()
                    for row in reversed(rows):
                        line = ','.join(row[:-1])+',"%s"' % row[-1].replace('"','""')+'\n'
                        counter = counter + len(line)
                        if counter<self.truncate or (row[-1].startswith('TASKNAME:') and tuple(row[2:4]) in tasks):
                            tasks.add(tuple(row[2:4]))
                            data = line+data
                dt=datetime.datetime.utcnow().isoformat().replace('T', ' ')[:23]
                data = '{datetime},,,,,,,"FILE TRUNCATED"\n'.format(datetime=dt) + data
                tmpfile = self.filename+'.tmp'
                with open(tmpfile, 'wb') as myfile:
                    myfile.write(data)
                os.rename(tmpfile, self.filename)

    def __getattr__(self, name):
        return (lambda text, *args: self.writelog(name, text, args))

    @staticmethod
    def catch_and_log(func):
        @wraps(func)
        def wrapper(*a, **b):
            try:
                return func(*a, **b)
            except Exception:
                Log.error(traceback.format_exc())
                raise
        return wrapper


class DummyErrorForTesting(object):
    def __str__(self):
        1/0

def test():

    dummy = DummyErrorForTesting()
    Log = SmartLogger('/tmp/testlog', maxsize=3e6, truncate=1e6,
                      console=True, callback=None)
    Log.info('TASKNAME:%s' % threading.currentThread().ident)
    for _ in range(10):
        for msg, args in [('test', []),
                          ('test %s',[1]),
                          ('test %(a)s',[{'a':2}]),
                          ('test %s', [dummy])]:
            Log.debug(msg, *args)
            Log.info(msg, *args)
            Log.warn(msg, *args)
            Log.error(msg, *args)
            Log.critical(msg, *args)

Log = SmartLogger('/tmp/testlog', maxsize=3e6, truncate=1e6, console=True, callback=None)

if __name__ == '__main__':
    Log = SmartLogger('/tmp/testlog', maxsize=3e6, truncate=1e6,
                      console=True, callback=None)
    import sys
    import multiprocessing
    if len(sys.argv) > 1:
        Log.error('this is a test')
    else:
        a = multiprocessing.Process(target = test)
        b = multiprocessing.Process(target = test)
        c = multiprocessing.Process(target = test)
        a.start()
        b.start()
        c.start()
        a.join()
        b.join()
        c.join()
