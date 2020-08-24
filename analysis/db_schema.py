#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Luca de Alfaro and Massimo Di Pierro
# License: BSD

# The Wikipedia DB is documented at
# https://upload.wikimedia.org/wikipedia/commons/9/94/MediaWiki_1.28.0_database_schema.svg

# Modified by Eric Vin, 2020

from .configuration import config
import datetime
import traceback
from .safelog import Log
from pydal.migrator import InDBMigrator
from pydal import DAL, Field

# TODO: read URI from a secrets/config.yaml type of file.
def connect_to_db(uri, migrate_enabled = False, fake_migrate_all=False):
    db = DAL(uri,
         migrate_enabled=migrate_enabled,
         fake_migrate_all=fake_migrate_all,
         adapter_args=dict(migrator=InDBMigrator),
         pool_size=10)

    db.define_table(
        # Environment is a group of pages that are linked such that reputation
        # is shared between them.
        'environment',

        # Plain text name for the environment
        Field('environment_name'),
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
        'user',

        Field('user_id', 'integer'), # The user_id is the same as on the wikipedia.

        Field('user_name'),
    )

    db.define_table(
        'revision',
        Field('revision_id', 'integer'), # On Wikipedia

        Field('user_id', 'integer'), # User id on the wikipedia for this user.

        Field('revision_date', 'datetime'),

        Field('revision_page', 'integer'),

        Field('prev_revision', 'integer'), #The revision before this one on the page
        # None if first revision for a page.

        Field('text_retrieved', 'boolean'), #True means retrieved, False means not retrieved

        Field('num_attempts', 'integer'), # To get markup from Wikipedia

        Field('last_attempt_date', 'datetime'), # Can also be a successful attempt.
    )

    # Stores what has been done on a revision and whether or not it is locked
    db.define_table(
        'revision_log',

        Field('page', 'reference page'),

        Field('algorithm'), # Which algorithm this log is in reference to.
        #(Text diff, Edit distance, Author rep, etc...)

        Field('last_revision', 'reference revision'), # Last revision analyzed.
        #I.E. How far we've gotten

        Field('lock_date', 'datetime'), # If null or old the page is not locked.
    )

    db.define_table(
        'user_reputation',

        # The user in question.
        Field('user_id', 'integer'),

        # The environment in which this reputation applies.
        Field('environment', 'reference environment'),

        # String identifier for algorithm that was run to determine this reputation
        Field('algorithm'),

        Field('reputation_value', 'double'),
    )

    db.define_table(
        'text_storage',

        Field('kind'), # markup, markup_w_rep, markup_w_author, ...

        Field('revision_id', 'integer'),

        Field('page_id', 'integer'),

        Field('revision_date', 'datetime'),

        Field('version'),

        Field('blob'), # name of GCS blob where info is stored.
    )

    # Cache for edit distance "triangles"
    db.define_table(
        'triangles',

        Field('page', 'reference page'),

        Field('algorithm'),

        Field('info', 'text'),
        # Json containing, for each previous revision p and subsequent revision f,
        # the distances in the triangle, and the user_ids of the authors.
        # {'revisions': [34, 35, 37], 'distances': [4.5, 5, 6.7], 'authors': [4, 5, 8], }
        # distances go 1-2, 1-3, 2-3

        Field('revid_1', 'integer'),
        Field('revid_2', 'integer'),
        Field('revid_3', 'integer'),

        Field('reputation_inc', 'double'), # How much the reputation was incremented
        # as a consequence of the triangle.  Set to null if triangle not processed.
        # This enables triangles to be processed twice. (check that we can query for null numbers).
    )

    # It is a good idea to cache the output of chdiff between consecutive revisions.

    # Cache for text_diff output
    # It is a good idea to cache the output of chdiff between consecutive revisions.
    db.define_table(
        'text_diff',

        Field('origin_revision_id', 'integer'),

        Field('dest_revision_id', 'integer'),

        #Note: origin_revision_id < dest_revision_id

        Field('info', 'text')
        #Text version of text_diff tuples between origin revision and dest revision

    )

    db.define_table('text_distance',
        Field('rev_1', 'integer'),
        Field('rev_2', 'integer'),
        Field('distance', 'double'),
        Field('info'), # Algorithm
    )

    return db


def create_indices(db):
    """Creates all the indices we need."""
    pass


def _create_idx(db):
    """Creates an index, rolling back if needed."""
    try:
        db.executesql('CREATE INDEX some_idx ON table(field, field)')
    except: db.rollback()
    db.commit()