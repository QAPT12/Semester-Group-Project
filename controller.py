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


def get_active_customers():
    """
    function to get all the customers who have had an invoice within the last month.

    :RETURNS:
        tuple: the resulting tuple containing the columns names and rows from the execute_query_return_results function
    """
    sql = "SELECT * FROM customers join invoices using(customer_id) WHERE order_date >= now() - INTERVAL 1 MONTH;"
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


"""
FUNCTIONS TO PREFORM ACTIONS ON THE INVENTORY
"""


def get_all_inventory_information_in_stock():
    """
    function for getting all inventory information of products in stock
    calls the execute_query_return_results function to return the column names and
    all the rows containing the information on inventory items.

    :RETURNS:
        tuple: the resulting tuple containing the column names and rows from the execute_query_return_results function.
    """
    sql = 'SELECT * FROM products WHERE products.in_stock > 0;'
    return execute_query_return_results(sql)


def get_all_inventory_information_out_stock():
    """
    function for getting all inventory information on products with no stock.
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
    sql = "SELECT invoice_id, customer_id, CONCAT(first_name, ' ', last_name) as name, order_date, invoice_total FROM " \
          "invoices i JOIN customers c using(customer_id) ORDER BY order_date DESC;"
    return execute_query_return_results(sql)


def get_invoice_items_by_invoice_id(invoice_id):
    """
    function for getting the information on the items belonging to an invoice.

    :PARAM:
        invoice_id: INT: the ID of the invoice that we want the line items for

    :RETURNS:
        tuple: the resulting tuple containing the column names and rows from the execute_query_return_results function.
    """
    assert type(invoice_id) == int, 'invoice id must be given as an int'
    sql = f"SELECT p.product_id, product_name, product_price, quantity FROM invoice_line_items il JOIN products p ON " \
          f"il.product_id = p.product_id where invoice_id = {invoice_id};"
    return execute_query_return_results(sql)


def get_invoice_information_by_id(invoice_id):
    """
    function for getting the information on an invoice from the invoice id.

    :PARAM:
        invoice_id: INT: the ID of the invoice that we want the line items for

    :RETURNS:
        tuple: the resulting tuple containing the column names and rows from the execute_query_return_results function.
    """
    assert type(invoice_id) == int, 'invoice id must be given as an int'
    sql = f"SELECT c.customer_id, CONCAT(first_name, ' ', last_name) as name, phone_number, email, home_address, " \
          f"order_date FROM invoices i JOIN customers c on i.customer_id = c.customer_id WHERE invoice_id = {invoice_id};"
    info = execute_query_return_results(sql)[1][0]
    invoice_info = {'customer_id': info[0], 'name': info[1], 'phone_number': info[2], 'email': info[3],
                    'address': info[4], 'date': info[5].strftime("%Y-%m-%d")}
    return invoice_info


def delete_invoice_by_id(invoice_id):
    """
    function to delete an invoice from the DB. uses the given invoice_id and calls the stored procedure to delete
    all invoice line items and invoices with the given invoice_id.

    :PARAM:
        invoice_id: int: the id of the invoice to be deleted

    :RETURNS:
        int: the resulting number of rows affected by the execute_query_commit function
    """
    assert type(invoice_id) == int, 'invoice id must be given as an int'
    sql = f"call the_athletic_outlet.delete_invoice_by_id({invoice_id});"
    return execute_query_commit(sql)
