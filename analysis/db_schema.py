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
        'environment',
        Field('environment'),
    )

    db.define_table(
        'page',
        Field('page_id', 'integer'), # On wikipedia
        Field('environment_id', 'reference environment', ondelete="SET NULL"),
        Field('page_title'),
        Field('analysis_time', 'datetime'),
    )

    db.define_table(
        'revision',
        Field('rev_id', 'integer'), # On wikipedia
        # user id on the wikipedia for this user.
        Field('user_id', 'integer'),
        Field('rev_date', 'datetime'),
        Field('rev_page', 'reference page'),
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

    db.define_table(
        'revision_block',
        Field('page_id', 'reference page'),
        # These fields are used to know in which order to stitch blocks
        # together, and also, if there are holes between them.
        # Id of the last revision before the block
        Field('prev_revision_id', 'integer'), # long??
        Field('next_revision_id', 'integer'),
        # To put blocks in chronological order by page.
        Field('initial_timestamp', 'datetime'),
        Field('storage_id'), # ID for S3 / GCS
    )

    db.define_table(
        'text_storage',
        Field('kind'), # markup, markup_w_rep, markup_w_author, ...
        Field('revision_id'),
        Field('page_id'),
        Field('blob_id'), # pointer to GCS or S3: name of the blob where the revision can be found.
    )

    db.define_table(
        'user_reputation',
        Field('user_id', 'reference user'),
        Field('topic id', 'reference topic', ondelete="SET NULL"),
        Field('block_id', 'reference revision_block'),
        Field('amount', 'double'),
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