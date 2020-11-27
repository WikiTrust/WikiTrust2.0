#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Luca de Alfaro and Massimo Di Pierro
# License: BSD

# The Wikipedia DB is documented at
# https://upload.wikimedia.org/wikipedia/commons/9/94/MediaWiki_1.28.0_database_schema.svg

# Modified by Eric Vin, 2020

#from configuration import config
import datetime
import traceback
#from safelog import Log
from pydal.migrator import InDBMigrator
from pydal import DAL, Field

# TODO: read URI from a secrets/config.yaml type of file.
def connect_to_db(uri = 'sqlite://volume/storage.sqlite'):
    db = DAL(uri,
        migrate=True,
        fake_migrate=False,
        migrate_enabled=True,
        fake_migrate_all=False,
        adapter_args=dict(migrator=InDBMigrator),
        pool_size=10)

    try:
        db.define_table(
            # Environment is a group of pages that are linked such that reputation.
            # is shared between them.
            'environment',
            # Plain text name for the environment.
            Field('environment_name')
        )
    except: pass

    try:
        db.define_table(
            'page',

            # Page ID on Wikipedia.
            Field('page_id', 'integer', unique = True),
            Field('environment_id', 'reference environment', ondelete="SET NULL"),
            Field('page_title'),
            # Datetime for last time revision puller checked this page for new revisions.
            # There may be more revisions after this date that we do not know about.
            Field('last_check_time', 'datetime'),
        )
    except: pass

    try:
        db.define_table(
            'user',

            # User ID on Wikipedia.
            Field('user_id', 'integer', unique = True),
            Field('user_name'),
        )
    except: pass

    try:
        db.define_table(
            'revision',

            # Various IDs on Wikipedia.
            Field('rev_id', 'integer', unique = True),
            Field('page_id', 'integer'),
            Field('user_id', 'integer'),
            # Datetime this revision was made on Wikipedia.
            Field('rev_date', 'datetime'),
            # The revision before this one on the page.
            # None if first revision for a page.
            Field('prev_rev', 'integer'),
            # True means retrieved, False means not retrieved.
            Field('text_retrieved', 'boolean'),
            # Datetime of last attempt to retrieve revision.
            # Can also be a successful attempt.
            Field('last_attempt_date', 'datetime'),
            # Number of attempts made to get markup from Wikipedia.
            Field('num_attempts', 'integer'),
        )
    except: pass

    try:
        # Tracks what stage a page is at in the Computation Engine
        db.define_table(
            'revision_log',

            # The Version of the code this is in reference to.
            Field('version'),
            # Which stage in the computation engine this log is in reference to.
            # (Text diff, Edit distance, Author rep, etc...).
            Field('stage'),
            # Page ID on Wikipedia.
            Field('page_id', 'integer'),
            # Revision ID on Wikipedia of last revision analyzed.
            Field('last_rev', 'integer'),
            # Datetime that this was locked.
            # If null or old the page is not locked.
            Field('lock_date', 'datetime'),
        )
    except: pass

    try:
        db.define_table(
            'user_reputation',

            # The Version of the code this is in reference to.
            Field('version'),
            # User ID on Wikipedia.
            Field('user_id', 'integer'),
            # The environment in which this reputation applies.
            Field('environment', 'reference environment'),
            # Double containing the reuptation of the user.
            Field('reputation_value', 'double'),
        )
    except: pass

    try:
        db.define_table(
            'text_storage',

            # The Version of the code that was used to generate the text.
            Field('version'),
            # Various IDs on Wikipedia.
            Field('page_id', 'integer'),
            Field('rev_id', 'integer'),
            # Kind of text being stored (markup, markup_w_rep, markup_w_author, ...).
            Field('text_type'),
            # Name of GCS blob where info is stored.
            Field('blob'),
        )
    except: pass

    try:
        # Cache for edit distance "triangles"
        db.define_table(
            'triangles',

            # The Version of the code that was used to generate the text.
            Field('version'),
            # Page ID on Wikipedia for the triangle's page.
            Field('page_id', 'integer'),
            # Revision IDs for three revisions in a triangle.
            Field('rev_id_1', 'integer'),
            Field('rev_id_2', 'integer'),
            Field('rev_id_3', 'integer'),
            # How much the reputation was incremented as a consequence of the triangle.
            # Set to null if triangle not processed.
            # This enables triangles to be processed twice. (Check that we can query for null numbers).
            Field('reputation_inc', 'double'),
        )
    except: pass

    try:
        # Cache for text difference.
        db.define_table(
            'text_diff',

            # The Version of the code that was used to generate the diff.
            Field('version'),
            # Revision IDs for difference.
            # Note: rev_id_1 < rev_id_2
            Field('rev_id_1', 'integer'),
            Field('rev_id_2', 'integer'),
            # Text version of text_diff tuples between rev_id_1 and rev_id_2
            Field('info', 'text')
        )
    except: pass

    try:
        db.define_table(
            'text_distance',

            # The Version of the code that was used to generate the distance.
            Field('version'),
            # Revision IDs for difference.
            # Note: rev_id_1 < rev_id_2
            Field('rev_id_1', 'integer'),
            Field('rev_id_2', 'integer'),
            # Numerical distance between rev_id_1 and rev_id_2.
            Field('distance', 'double'),
        )
    except: pass

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