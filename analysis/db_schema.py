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

def define_tables(uri, migrate_enabled = False, fake_migrate_all=False):
    db = DAL(uri,
             migrate_enabled=migrate_enabled,
             fake_migrate_all=fake_migrate_all,
             adapter_args=dict(migrator=InDBMigrator),
             pool_size=10)


    old_date = datetime.datetime(year=1980, month=1, day=1)

    ### Wikipedia Data Tables ###

    db.define_table(
        # Environment is a group of pages that are linked such that reputation
        # is shared between them.
        'environment',

        # Unique id for the environment
        Field('environment_id', 'integer'),

        # Plain text name for the environment
        Field('environment_name'),
    )

    db.define_table(
        'page',

        Field('page_id', 'integer'),
        Field('page_title'),

        # A reference to the environment the page is a part of
        Field('page_environment', 'reference environment'),

        # We want to analyze this page only from this date onwards.  If None, then
        # analyze from the beginning.
        Field('analysis_start_time', 'datetime'),
    )

    db.define_table(
        'user',

        # The user_id is the same as on the wikipedia.
        Field('user_id', 'integer'),
        Field('user_name'),
        Field('user_real_name'),
    )

    db.define_table(
        'revision',

        Field('rev_id', 'integer'),

        # Reference to user who made the revision.
        Field('user', 'reference user'),

        Field('rev_date', 'datetime'),
        Field('rev_page', 'reference page'),

        # File name for a the compressed block in GCS and the offset where
        # the revision is present inside that block.
        Field('rev_file_name'),
        Field('rev_file_offset'),

        # NOTE: Plan to use static caching for reputation-annotated text instead, as
        # it is never used in any other calculations.
        # ID of a blob in GCS or S3 where the reputation-annotated text can be found.
        # Field('annotated_text'),

        # Date at which the annotation has been computed, used to estimate whether
        # it should be recomputed.
        Field('annotation_date', 'datetime'),
    )


    ### User Reputation Tables ###

    db.define_table(
        'user_reputation',

        # The user in question.
        Field('user', 'reference user'),

        #The environment in which this reputation applies.
        Field('environment', 'reference environment'),

        Field('reputation', 'double'),
    )

    ### Cache tables ###

    db.define_table(
        'edit_distance',

        # Note: revision_id_1 < revision_id_2
        Field('revision_id_1', 'integer'),
        Field('revision_id_2', 'integer'),

        Field('distance', 'double'),
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