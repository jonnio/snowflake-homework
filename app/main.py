import concurrent.futures
import math
import os
from time import sleep

import snowflake.connector
from fastapi import FastAPI, Query
from pydantic import BaseModel
from snowflake.connector import DictCursor

app = FastAPI()

con = snowflake.connector.connect(
    user='HOMEWORK_USER',
    password=os.environ.get('SNOWFLAKE_PASSWORD', 'NONE'),
    account='iloovmp-gx92880',
    warehouse='HOMEWORK_WH',
    database='SNOWFLAKE_SAMPLE_DATA',
    schema='TPCH_SF10',
    session_parameters={
        'QUERY_TAG': 'TAG_HOMEWORK',
    }
)


class SnowflakePage(BaseModel):
    items: list = []
    limit: int = 0
    page: int = 0
    total: int = 0
    count: int = 0


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


@app.get('/customer/list', tags=['customer'])
async def get_customers(limit: int = Query(default=10, le=100, gt=0), page: int = Query(default=0, ge=0)) -> SnowflakePage:
    response_page = SnowflakePage(limit=limit, page=page)

    def run_query(q_cursor, statement, params):
        query = q_cursor.execute_async(statement, params, ) if params else q_cursor.execute_async(statement)
        while con.is_still_running(con.get_query_status(query['queryId'])):
            sleep(0.3)
        q_cursor.get_results_from_sfqid(query['queryId'])
        records = q_cursor.fetchall()
        print('returning %d records', len(records))
        return records

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_query, con.cursor(cursor_class=DictCursor),
                                   "SELECT * FROM CUSTOMER ORDER BY C_CUSTKEY LIMIT %s OFFSET %s",
                                   (limit, (page * limit + limit),)),
                   executor.submit(run_query, con.cursor(cursor_class=DictCursor),
                                   "SELECT COUNT(*) AS X_COUNT FROM CUSTOMER",
                                   ()),
                   ]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if len(data) == 1 and isinstance(data[0], dict) and 'X_COUNT' in data[0]:
                response_page.total = math.floor(data[0].get('X_COUNT', 0) / limit) - 1
            else:
                response_page.items = data
                response_page.count = len(data)

    return response_page


@app.get('/customer/{customer_id}', tags=['customer'])
async def get_customer(customer_id: str):
    print(customer_id)
    cursor = con.cursor(cursor_class=DictCursor)
    sql = cursor.execute("SELECT * FROM CUSTOMER WHERE 1=1 and C_CUSTKEY=%s", (customer_id,))
    return sql.fetchall()
