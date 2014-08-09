from queries import Queries as q
from exceptions import NotPostgresEngine

try:
    from sqlalchemy.exc import ProgrammingError
except ImportError:
    print 'Sqlalchemy not installed in this system.'

def pghero(toolkit, db):
    if toolkit == 'sqlalchemy':
        return SqlAlchemyPgHero(db)

class PgHeroBase():
    pass

class SqlAlchemyPgHero(): # TODO: inherit from base class

    def __init__(self, db):
        self.db = db
        if not self.is_pg():
            raise NotPostgresEn('Database engine should be postgres')
    
    def running_queries(self):
        return self.select_all(q.running_queries)

    def long_running_queries(self):
        return self.select_all(q.long_running_queries)
    
    def index_hit_rate(self):
        return float(self.select_all(q.index_hit_rate)[0])
    
    def table_hit_rate(self):
        return float(self.select_all(q.table_hit_rate)[0])

    def index_usage(self):
        return self.select_all(q.index_usage)

    def missing_indexes(self):
        return self.select_all(q.missing_indexes)

    def unused_tables(self):
        return self.select_all(q.unused_tables)

    def unused_indexes(self):
        return self.select_all(q.unused_indexes)

    def relation_sizes(self):
        return self.select_all(q.relation_sizes)

    def database_size(self):
        return self.select_all(q.database_size)
    
    def slow_queries(self):
        if self.query_stats_enabled():
            return self.select_all(q.slow_queries)
        return []

    #def query_stats_enabled(self):
    #    qse = self.select_all(q.query_stats_enabled)
    #    qsr = self.query_stats_readable()
    #    print  (qse, qsr)
    #    return qse and qsr
    
    def query_stats_readable(self):
        try:
            return self.select_all(q.query_stats_readable)
        except ProgrammingError:
            return False

    def is_pg(self):
        return self.db.engine.name == 'postgresql'

    def enable_query_stats(self):
        self.execute(q.enable_query_stats)
        return True

    def disable_query_stats(self):
        self.execute(q.disable_query_stats)
        return True

    def select_all(self, sql):
        result = self.execute(sql).fetchall()
        result = list(self.execute(sql).fetchall())
        if result == []:
            return []
        return filter(None, result[0])

    def execute(self, sql):
        return self.db.engine.execute(sql)

