import psycopg2 as pg
from psycopg2.extras import DictCursor
import json

class DataBase:
    def __init__(self):
        self.conn = pg.connect(database = 'postgres')
        self.cur = self.conn.cursor(cursor_factory=DictCursor)

    def execute(self, query, post=False):
        try:
            print(query)
            self.cur.execute(query)
            self.conn.commit()
            return self.cur.rowcount if post else [dict(record) for record in self.cur]
        except Exception as e:
            return str(e)
