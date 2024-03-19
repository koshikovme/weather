import sqlite3
from enum import Enum
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB

def get_connection():
    try:
        con = sqlite3.connect(
           "./database.db" 
        )
        return con
    except Exception as e:
        print("Connection unsuccessful")
        print(e)
        raise e

class FetchMode(Enum):
    one = "one"
    many = "many"
    all = "all"

def execute(
    stmt: str,
    values: tuple = (),
    is_commitable: bool = False,
    is_fetchable: bool = False,
    fetch_strategy: FetchMode = FetchMode.one,
    fetch_size: int = 5,
):
    con = get_connection()
    cursor = con.cursor()

    cursor.execute(stmt, values)

    res = None
    if is_fetchable:
        if fetch_strategy == FetchMode.one:
            res = cursor.fetchone()
        elif fetch_strategy == FetchMode.many:
            res = cursor.fetchmany(size=fetch_size)
        elif fetch_strategy == FetchMode.all:
            res = cursor.fetchall()

    if is_commitable:
        con.commit()

    cursor.close()
    con.close()

    return res if is_fetchable else None  # Return None if not fetchable

