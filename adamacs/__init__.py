import datajoint as dj
import pathlib

default_prefix = 'adamacs_'

if 'custom' not in dj.config:
    dj.config['custom'] = {}


db_prefix = dj.config['custom'].get('database.prefix', default_prefix)
