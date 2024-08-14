import concurrent.futures
import math
from time import sleep

from pydantic import BaseModel
from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import DictCursor


class SnowflakePage(BaseModel):
    items: list = []
    limit: int = 0
    page: int = 0
    total: int = 0
    count: int = 0


def get_page(connection: SnowflakeConnection,
             query: str,
             limit: int,
             page: int,
             args: (),
             count_table_name: str = None) -> SnowflakePage:
    def run_query(q_cursor, statement, params):
        query = q_cursor.execute_async(statement, params, ) if params else q_cursor.execute_async(statement)
        while connection.is_still_running(connection.get_query_status(query['queryId'])):
            sleep(0.12)
        q_cursor.get_results_from_sfqid(query['queryId'])
        records = q_cursor.fetchall()
        return records

    response_page = SnowflakePage(limit=limit, page=page)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_query, connection.cursor(cursor_class=DictCursor),
                                   query + " LIMIT %s OFFSET %s",
                                   args + (limit, (page * limit + limit),)),
                   ]
        if count_table_name:
            futures.append(executor.submit(run_query, connection.cursor(cursor_class=DictCursor),
                                           f"SELECT COUNT(*) AS X_COUNT FROM {count_table_name}",
                                           ()))
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if len(data) == 1 and isinstance(data[0], dict) and 'X_COUNT' in data[0]:
                response_page.total = math.floor(data[0].get('X_COUNT', 0) / limit) - 1
            else:
                response_page.items = data
                response_page.count = len(data)

    return response_page
