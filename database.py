import psycopg2 as pg
from psycopg2.extras import DictCursor
import json

class DataBase:
    def __init__(self):
        self.conn = pg.connect(host='postgre-docapp.postgres.database.azure.com', password='azure@2020', port='5432', sslmode=True, dbname='docker', user='postgres@postgre-docapp')
        self.cur = self.conn.cursor(cursor_factory=DictCursor)

    def execute(self, query, post=False):
        try:
            self.cur.execute(query)
            self.conn.commit()
            if post:
                return self.cur.rowcount
            else:
                return [dict(record) for record in self.cur]
        except Exception as e:
            self.conn.rollback()
            return str(e)
