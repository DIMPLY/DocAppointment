import psycopg2 as pg
from psycopg2.extras import DictCursor
import json

class DataBase:
    def __init__(self):
        self.conn = pg.connect(host='database-docapp.c7slslxxnqtk.us-west-1.rds.amazonaws.com', password='postgres', port='5432', dbname='docker', user='postgres')
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
