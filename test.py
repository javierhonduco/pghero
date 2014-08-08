from core import pghero

from sqlalchemy import create_engine

db_path = 'postgres://javierhonduco@localhost:5432/tw'

db = create_engine(db_path)

print db.engine.name

pghero = pghero('sqlalchemy', db)

print pghero.running_queries()
print
print pghero.long_running_queries()
print 
print pghero.index_hit_rate()
print
print pghero.table_hit_rate()
print
print pghero.index_usage()
print 
print pghero.missing_indexes()
print
print pghero.unused_tables()
print
print pghero.unused_indexes()
print
print pghero.relation_sizes()
print
print pghero.database_size()
print
