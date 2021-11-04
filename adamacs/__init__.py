import datajoint as dj

default_prefix = 'adamacs_'

db_prefix = dj.config.get('custom', {}).get('database.prefix', default_prefix)
