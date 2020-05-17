import psycopg2 as pg
from psycopg2.extras import DictCursor
import json

# dbname='{your_database}' user='postgres@postgre-docapp' host='postgre-docapp.postgres.database.azure.com' password='{your_password}' port='5432' sslmode='true'
conn = pg.connect(host='database-docapp.c7slslxxnqtk.us-west-1.rds.amazonaws.com', password='postgres', port='5432', user='postgres')
conn.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
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

res = execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'docker'")
print('docker', res)
if not res:
    print(execute("CREATE DATABASE docker", True))
    execute("CREATE EXTENSION \"uuid-ossp\"")
else:
    print('docker already exists')
cur.close()
conn.close()
conn = pg.connect(host='database-docapp.c7slslxxnqtk.us-west-1.rds.amazonaws.com', database='docker', password='postgres', port='5432', user='postgres')
cur = conn.cursor(cursor_factory=DictCursor)

f = open("db_init.txt")
for db in f.read().split("\n\n"):
    res = execute("SELECT 1 FROM pg_tables WHERE tablename = '{}'".format(db.split()[0]))
    print(db.split()[0], res)
    if not res:
        print(execute("CREATE TABLE " + "".join(db.split("\n")), True))

res = execute("SELECT 1 FROM pg_tables WHERE tablename = 'numbers'")
if not res:
    print(execute("INSERT INTO numbers VALUES " + ", ".join("({})".format(i) for i in range(1, 601)), True))
cur.close()
conn.close()
