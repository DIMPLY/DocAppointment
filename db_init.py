import psycopg2 as pg
from psycopg2.extras import DictCursor
import json


conn = pg.connect(database='docker', user='postgres')
cur = conn.cursor(cursor_factory=DictCursor)

def execute(query, post=False):
    print("Executing:", query)
    try:
        cur.execute(query)
        conn.commit()
        if post:
            return cur.rowcount
        else:
            return [dict(record) for record in cur]
    except Exception as e:
        conn.rollback()
        return str(e)

f = open("db_init.txt")
for db in f.read().split("\n\n"):
    execute("CREATE TABLE IF NOT EXISTS " + "".join(db.split("\n")), True)

execute("INSERT INTO numbers VALUES " + ", ".join("({})".format(i) for i in range(1, 601)), True)

