import psycopg2 as pg
from psycopg2.extras import DictCursor
import json

# dbname='{your_database}' user='postgres@postgre-docapp' host='postgre-docapp.postgres.database.azure.com' password='{your_password}' port='5432' sslmode='true'
conn = pg.connect(host='postgre-docapp.postgres.database.azure.com', password='azure@2020', port='5432', sslmode='true', user='postgres@postgre-docapp')
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

execute("CREATE DATABASE IF NOT EXISTS docker", True)
f = open("db_init.txt")
for db in f.read().split("\n\n"):
    execute("CREATE TABLE IF NOT EXISTS " + "".join(db.split("\n")), True)

execute("INSERT INTO numbers VALUES " + ", ".join("({})".format(i) for i in range(1, 601)), True)
cur.close()
conn.close()
