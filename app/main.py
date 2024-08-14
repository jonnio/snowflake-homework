import os

import snowflake.connector
from fastapi import FastAPI, Query
from snowflake.connector import DictCursor

from app.pagination import get_page, SnowflakePage

description = """
This is part of the Snowflake Homework for Jon Osborn 🚀

## Root

You can get **root content** or **get tables** as a list.

## Customer

You will be able to:

* **list customers**
* **get customer** by id
"""

app = FastAPI(title="Snowflake Homework - Osborn",
              description=description,
              summary="Jon Osborn's Snowflake Homework",
              version="0.0.1",
              contact={
                  "name": "Jon Osborn",
                  "url": "https://www.linkedin.com/in/jonosborn/",
                  "email": "osborn.jon.20@gmail.com",
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              }, )

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


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to my homework",
            "version": 1,
            }


@app.get('/tables', tags=['root'], description="Retrieve a list of tables")
async def get_tables():
    cursor = con.cursor()
    sql = cursor.execute("SHOW TERSE TABLES IN SCHEMA TPCH_SF10")
    return sorted(set([t[1] for t in sql]))


@app.get('/customer/list', tags=['customer'], description="List customers by page")
async def get_customers(limit: int = Query(default=10, le=100, gt=0), page: int = Query(default=0, ge=0)) -> SnowflakePage:
    return get_page(con,
                    "SELECT * FROM CUSTOMER ORDER BY C_CUSTKEY",
                    limit,
                    page,
                    (),
                    "CUSTOMER")


@app.get('/customer/{customer_id}', tags=['customer'], description="Get a customer by id")
async def get_customer(customer_id: str):
    cursor = con.cursor(cursor_class=DictCursor)
    sql = cursor.execute("SELECT * FROM CUSTOMER WHERE 1=1 AND C_CUSTKEY=%s", (customer_id,))
    return sql.fetchall()


@app.get('/order/summary', tags=['order'], description="Get a summary of orders by customer")
async def get_order_summary(limit: int = Query(default=10, le=100, gt=0), page: int = Query(default=0, ge=0)) -> SnowflakePage:
    return get_page(con,
                    ("SELECT C.C_NAME, C.C_CUSTKEY\n"
                     ",COALESCE(COUNT(O.O_ORDERKEY), 0) AS NUM_ORDERS\n"
                     ",COALESCE(SUM(O.O_TOTALPRICE),0)::NUMERIC(18,2) AS ORDER_TOTAL_PRICE\n"
                     ",COALESCE(SUM(O.O_TOTALPRICE),0)::NUMERIC(18,2) AS ORDER_AVERAGE_PRICE, MIN(O.O_ORDERDATE) AS FIRST_ORDER_DATE\n"
                     ",MAX(O.O_ORDERDATE) AS LAST_ORDER_DATE\n"
                     ",SUM(CASE WHEN O.O_ORDERSTATUS = 'F' THEN 1 ELSE 0 END) AS F_ORDERS\n"
                     ",SUM(CASE WHEN O.O_ORDERSTATUS = 'O' THEN 1 ELSE 0 END) AS O_ORDERS\n"
                     "FROM CUSTOMER C \n"
                     "LEFT JOIN ORDERS O ON O.O_CUSTKEY=C.C_CUSTKEY\n"
                     "GROUP BY ALL\n"
                     "ORDER BY C.C_NAME"),
                    limit,
                    page,
                    (),
                    "CUSTOMER", )


@app.get('/order/{order_id}', tags=['order'], description="Get a specific order")
async def get_order(order_id: int):
    return (con
            .cursor(cursor_class=DictCursor)
            .execute("SELECT * FROM ORDERS WHERE O_ORDERKEY = %s", (order_id,))
            .fetchall())


@app.get('/order/{order_id}/details', tags=['order'], description="Get order details")
async def get_order(order_id: int):
    return (con
            .cursor(cursor_class=DictCursor)
            .execute(("SELECT *"
                      " FROM LINEITEM "
                      " WHERE L_ORDERKEY = %s"
                      " ORDER BY L_PARTKEY"), (order_id,))
            .fetchall())
