from queries import Queries as q
from exceptions import NotImplementedError #NotPostgresEngine

class PgHero:
    pass

class SqlAlchemyPgHero(): # TODO: inherit from base class

    def __init__(self, db):
        self.db = db
        if not self.is_pg():
            raise Exception('Database engine should be postgres')
    
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
    
    def is_pg(self):
        return self.db.engine.name == 'postgresql'
    
    def select_all(self, sql):
        result = self.execute(sql).fetchall()
        result = list(self.execute(sql).fetchall())
        if result == []:
            return []
        return filter(None, result[0])

    def execute(self, sql):
        return self.db.engine.execute(sql)

