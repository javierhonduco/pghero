from queries import Queries as q

class PgHero:
    pass

class SqlAlchemyPgHero(): # TODO: inherit from base classº

    def __init__(db):
        self.db = db
        if not self.is_pg():
            raise Exception('Database engine should be postgres')
    
    def running_queries(self):
        return self.execute(q.running_queries).fetchall()

    def long_running_queries(self):
        return self.execute(q.long_running_queries).fetchall()
    
    def index_hit_rate(self):
        return self.execute(q.index_hit_rate).fetchall()
    
    def table_hit_rate(self):
        return self.execute(q.table_hit_rate).fetchall()

    def index_usage(self):
        return self.execute(q.usage).fetchall()

    def missing_indexes(self):
        return self.execute(q.missing_indexes).fetchall()

    def unused_tables(self):
        return self.execute(q.unused_tables).fetchall()

    def unused_indexes(self):
        return self.execute(q.unused_indexes).fetchall()

    def relation_sizes(self):
        return self.execute(q.relation_sizes).fetchall()

    def database_size(self):
        return self.execute(q.database_size).fetchall()
    
    def is_pg(self):
        return self.db.engine.name == 'postgres'

    def execute(self):
        return self.db.engine.execute


#pghero = PgHero() # TODO. Add example. Pass instance of SA
#pghero.running_queries()
