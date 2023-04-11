from generic_sql import execute_query_return_results
from generic_sql import execute_query_commit

"""
FUNCTIONS TO PERFORM ACTIONS ON THE CUSTOMERS
"""


def get_all_customer_information():
    """
    function for getting all customer information.
    calls the execute_query_return_results function to return the column names and 
    all the rows containing the customer information.

    :RETURNS:
        tuple: the resulting tuple containing the column names and rows from the execute_query_return_results function.
    """
    sql = 'SELECT * FROM customers;'
    return execute_query_return_results(sql)


def get_customer_information_by_id(customer_id):
    """
    function called for when you want the information on a specific customer, useful for when you want to perform an update or delete.

    :PARAM:
        customer_id: INT: the id of the customer you wish to get the information on.

    :RETURNS:
        dict: a dictionary containing all the information for the customer with the given id.
    """
    assert type(customer_id) == int, 'given value for customer id must be an INT'
    sql = f'SELECT * FROM customers WHERE customer_id = {customer_id}'
    results = execute_query_return_results(sql)[1]
    customer_information = {'customer_id': results[0][0], 'first_name': results[0][1], 'last_name': results[0][2],
                            'phone_number': results[0][3], 'email': results[0][4], 'address': results[0][5]}
    return customer_information


def add_customer(first_name, last_name, phone_number, email, address):
    """
    function called when you want to add a customer to the DB.

    :PARAM:
        first_name: str: the first name of the customer.
        last_name: str: the last name of the customer.
        phone_number: str: phone number of the customer.
        email: str: email for the customer.

    :RETURNS: 
        int: the count of the rows affected from the execute_query_commit function
    """
    sql = f"INSERT INTO customers VALUES (default, '{first_name}', '{last_name}', '{phone_number}', '{email}', '{address}')"
    return execute_query_commit(sql)

def delete_customer_by_id(customer_id):
    """
    function to delete a customer using the given customer id.

    :PARAM:
        customer_id: int: the id of the customer you wish to delete.

    :RETURNS:
        int: the count of the affected rows from the execute_query_commit function
    """
    sql = f'DELETE FROM customers WHERE customer_id = {customer_id}'
    return execute_query_commit(sql)


def get_active_customers():
    """
    function to get all the customers who have had an invoice within the last month.

    :RETURNS:
        tuple: the resulting tuple containing the columns names and rows from the execute_query_return_results function
    """
    sql = "SELECT customer_id, CONCAT(first_name, ' ', last_name) as name, phone_number, email, home_address FROM customers join " \
          "invoices using(customer_id) WHERE order_date >= now() - INTERVAL 1 MONTH;"
    return execute_query_return_results(sql)


"""
FUNCTIONS TO PREFORM ACTIONS ON THE INVENTORY
"""


def get_all_inventory_information_in_stock():
    """
    function for getting all inventory information.
    calls the execute_query_return_results function to return the column names and 
    all the rows containing the information on inventory items.

    :RETURNS:
        tuple: the resulting tuple containing the column names and rows from the execute_query_return_results function.
    """
    sql = 'SELECT * FROM products WHERE products.in_stock > 0;'
    return execute_query_return_results(sql)


def get_all_inventory_information_out_stock():
    """
    function for getting all inventory information.
    calls the execute_query_return_results function to return the column names and 
    all the rows containing the information on inventory items.

    :RETURNS:
        tuple: the resulting tuple containing the column names and rows from the execute_query_return_results function.
    """
    sql = 'SELECT * FROM products WHERE products.in_stock <= 0;'
    return execute_query_return_results(sql)

"""
FUNCTIONS TO PERFORM ACTIONS ON INVOICES
"""


def get_all_invoice_information():
    """
    function for getting all the information on the invoices.
    calls the execute_query_return_results function to return the column names and
    all the rows containing the information on the invoices.

    :RETURNS:
        tuple: the resulting tuple containing the column names and rows from the execute_query_return_results function.
    """
    sql = 'SELECT * FROM invoices;'
    return execute_query_return_results(sql)
