import os

import snowflake.connector
from fastapi import FastAPI

app = FastAPI()

con = snowflake.connector.connect(
    user='HOMEWORK_USER',
    password=os.environ.get('SNOWFLAKE_PASSWORD', 'NONE'),
    account='iloovmp-gx92880',
    warehouse='HOMEWORK_WH',
    database='SNOWFLAKE_SAMPLE_DATA',
    SCHEMA='TPCH_SF10',
    session_parameters={
        'QUERY_TAG': 'TAG_HOMEWORK',
    }
)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World",
            "version": 1,
            }


@app.get('/tables', tags=['root'])
async def get_tables():
    cursor = con.cursor()
    sql = cursor.execute("SHOW TERSE TABLES")
    return sorted(set([t[1] for t in sql]))
