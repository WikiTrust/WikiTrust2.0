#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Luca de Alfaro and Massimo Di Pierro
# License: BSD

# This file contains the setup of the metadata database.

from .configuration import config, secrets
from .db_schema import define_tables, create_indices
from functools import wraps
from pydal import DAL, Field
from .safelog import Log
import traceback


def reconnecting(func):
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        return ret
    return decorated_function


def autocommit(func):
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        try:
            ret = func(self, *args, **kwargs)
        except:
            Log.error(traceback.format_exc())
            self.db.rollback()
            raise
        self.db.commit()
        return ret
    return decorated_function



class DataInterface(object):

    def __init__(self, uri=None, update_tables=False, create_indexes=False, fake_migrate_all=False):
        """Creates a data interface.  If uri is None, then uses a test sqlite
        database."""
        self.uri = uri or secrets[config['database']]['uri']
        Log.info("Using db uri: %r", self.uri)
        self.db = define_tables(
            self.uri, migrate_enabled=update_tables or fake_migrate_all, fake_migrate_all=fake_migrate_all)
        if fake_migrate_all:
            self.db.commit()
        if create_indexes:
            self.db.commit()
            create_indexes(self.db)


# Page table



# Revision blocks