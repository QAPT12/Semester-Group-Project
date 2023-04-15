import mysql.connector
from information import USER
from information import PASS
from information import HOST
from information import PORT


def execute_query_return_results(query, host=HOST, username=USER, password=PASS, port=PORT,
                                 database='the_athletic_outlet'):
    """
    generic sql function for selecting data from a table.

    :PARAM: 
        query: SQL query to be executed
        host: host of the server, localhost by default
        username: user being used to access the DB, default is set in the USER variable 
        password: pass for the user being used to access the DB, defualt is set in the PASS variable
        port: port to access the DB through, default is 3306
        database: the name pf the database being connected to, in our acse default is the_athletic_outlet

    :RETURNS:
        a tuple containing two tuples, the first being the column names, and the second being the rows returned from the query.
    """
    with mysql.connector.connect(host=host, user=username, password=password, port=port,
                                 database=database) as connector:
        with connector.cursor() as cursor:
            cursor.execute(query)
            return cursor.column_names, cursor.fetchall()


def execute_query_commit(query, host=HOST, username=USER, password=PASS, port=PORT,
                         database='the_athletic_outlet'):
    """
    generic sql function to make a change to the DB(UPDATE, DELETE, INSERT, etc.)

    :PARAM: 
        query: SQL query to be executed
        host: host of the server, localhost by default
        username: user being used to access the DB, default is set in the USER variable 
        password: pass for the user being used to access the DB, default is set in the PASS variable
        port: port to access the DB through, default is 3306
        database: the name of the database being connected to, in our case default is the_athletic_outlet

    :RETURNS:
        returns the number of rows affected by the query
    """
    with mysql.connector.connect(host=host, user=username, password=password, port=port,
                                 database=database) as connector:
        with connector.cursor() as cursor:
            cursor.execute(query)
            connector.commit()
            return cursor.rowcount
