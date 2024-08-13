import decimal
import os
import json

import snowflake.connector
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from snowflake.connector import DictCursor
from starlette.responses import JSONResponse

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
    sql = cursor.execute("SHOW TERSE TABLES IN SCHEMA TPCH_SF10")
    return sorted(set([t[1] for t in sql]))


@app.get('/customer', tags=['customer'])
async def get_customers():
    cursor = con.cursor(cursor_class=DictCursor)
    sql = cursor.execute("SELECT * FROM TPCH_SF10.CUSTOMER LIMIT 10")
    return sql.fetchall()


@app.get('/customer/{customer_id}', tags=['root'])
async def get_customer(customer_id: str):
    print(customer_id)
    cursor = con.cursor(cursor_class=DictCursor)
    sql = cursor.execute("SELECT * FROM TPCH_SF10.CUSTOMER WHERE 1=1 and C_CUSTKEY=%s", (customer_id,))
    return sql.fetchall()
