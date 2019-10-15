#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Luca de Alfaro and Massimo Di Pierro
# License: BSD

# The Wikipedia DB is documented at
# https://upload.wikimedia.org/wikipedia/commons/9/94/MediaWiki_1.28.0_database_schema.svg

from .configuration import config
import datetime
import traceback
from .safelog import Log
from pydal.migrator import InDBMigrator
from pydal import DAL, Field

def define_tables(uri, migrate_enabled = False, fake_migrate_all=False):
    db = DAL(uri,
             migrate_enabled=migrate_enabled,
             fake_migrate_all=fake_migrate_all,
             adapter_args=dict(migrator=InDBMigrator),
             pool_size=10)


    old_date = datetime.datetime(year=1980, month=1, day=1)

    db.define_table(
        'page',
        Field('page_id', 'integer'),
        Field('page_title'),
        # We want to analyze this page only from this date onwards.  If None, then
        # analyze from the beginning.
        Field('analysis_start_time', 'datetime'),
    )

    db.define_table(
        'revision',
        Field('rev_id', 'integer'),
        # user id on the wikipedia for this user.
        Field('user_id', 'integer'),
        Field('rev_date', 'datetime'),
        Field('rev_page', 'reference page'),
        # ID of a blob in GCS or S3 where the text can be found.
        Field('rev_text'),
        # ID of a blob in GCS or S3 where the reputation-annotated text can be found.
        Field('annotated_text'),
        # Date at which the annotation has been computed, used to estimate whether
        # it should be recomputed.
        Field('annotation_date', 'datetime'),
    )

    db.define_table(
        'user',
        # The user_id is the same as on the wikipedia.
        Field('user_id', 'integer'),
        Field('user_name'),
        Field('user_real_name'),
        # Value of reputation
        Field('reputation', 'double'),
    )





def create_indices(db):
    """Creates all the indices we need."""
    pass


def _create_idx(db):
    """Creates an index, rolling back if needed."""
    try:
        db.executesql('CREATE INDEX some_idx ON table(field, field)')
    except: db.rollback()
    db.commit()