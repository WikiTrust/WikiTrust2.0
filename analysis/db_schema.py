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
        Field('last_check_time', 'datetime'), # Of last check on Wikipedia,
        # there may be more revisions after this date that we do not know about.
    )

    db.define_table(
        'revision',
        Field('revision_id', 'integer'), # On wikipedia
        # user id on the wikipedia for this user.
        Field('user_id', 'integer'),
        Field('revision_date', 'datetime'),
        Field('page_id', 'integer'), # On wikipedia
        Field('revision_page', 'reference page'),
        Field('revision_blob'), # On GCS
        Field('has_text', 'boolean'),
        Field('num_attempts', 'integer'), # To get markup from Wikipedia
        Field('last_attempt_date', 'datetime'), # Can also be a successful attempt.
    )

    db.define_table(
        'revision_log', # Stores what has been done on a revision
        Field('page', 'reference page'),
        Field('algorithm'), # Which algo: text diff, auth rep, text rep, authorship, ... with version
        Field('last_revision', 'reference revision'), # Analyzed.
        Field('lock_date', 'datetime'), # if null or old the page is not locked.
    )

    db.define_table(
        'text_storage',
        Field('kind'), # markup, markup_w_rep, markup_w_author, ...
        Field('revision_id'),
        Field('page_id'),
        Field('revision_date', 'datetime'),
        Field('version'),
        Field('blob'), # name of GCS blob where info is stored.
    )

    db.define_table(
        'triangles',
        Field('page', 'reference page'),
        Field('algorithm'),
        Field('info', 'text'),
        # Json containing, for each previous revision p and subsequent revision f,
        # the distances in the triangle, and the user_ids of the authors.
        # {'revisions': [34, 36, 37], 'distances': [4.5, 5, 6.7], 'authors': [4, 5, 8], }
        Field('triangle_date', 'datetime'), # of last revision (check)
        Field('reputation_inc', 'double'), # How much the reputation was incremented
        # as a consequence of the triangle.  Set to null if triangle not processed.
        # This enables triangles to be processed twice. (check that we can query for null numbers).
    )

    # It is a good idea to cache the output of chdiff between consecutive revisions.

    db.define_table(
        'reputation',
        Field('user', 'reference user'),
        Field('environment', 'reference environment'),
        Field('algorithm'),
        Field('reputation_value', 'double'),

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