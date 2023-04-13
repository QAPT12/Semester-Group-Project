from PyQt6 import uic
from PyQt6.QtWidgets import *
import sys
from controller import *
from datetime import date


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)
        self.pos_customer_items = {}

        self.initialize_pos_tab()

        self.initialize_inventory_tab()

        self.initialize_customers_tab()

        self.initialize_invoices_tab()

        self.populate_all_tables()

        self.populate_all_combo_boxes()

    """
    VVVV METHODS FOR THE POS TAB VVVV
    """

    def initialize_pos_tab(self):
        """
        initializes the tables and widgets located on the POS tab of the GUI
        """
        self.tbl_pos_invoice = self.findChild(QTableWidget, 'tbl_pos_invoice')

        self.lbl_pos_total_price = self.findChild(QLabel, 'lbl_pos_total_price')
        self.lbl_pos_results = self.findChild(QLabel, 'lbl_pos_results')

        self.btn_pos_checkout = self.findChild(QPushButton, 'btn_pos_checkout')
        self.btn_pos_checkout.clicked.connect(self.btn_pos_checkout_click_handler)

        self.btn_pos_add_item = self.findChild(QPushButton, 'btn_pos_add_item')
        self.btn_pos_add_item.clicked.connect(self.btn_pos_add_item_click_handler)

        self.btn_pos_remove_item = self.findChild(QPushButton, 'btn_pos_remove_item')
        self.btn_pos_remove_item.clicked.connect(self.btn_pos_remove_item_click_handler)

        self.cmb_pos_items = self.findChild(QComboBox, 'cmb_pos_items')

        self.cmb_pos_customer = self.findChild(QComboBox, 'cmb_pos_customer')
        self.cmb_pos_customer.currentIndexChanged.connect(self.cmb_pos_customer_change_handler)

        self.spb_pos_item_amount = self.findChild(QSpinBox, 'spb_pos_item_amount')

        self.txt_pos_customer_phone = self.findChild(QLineEdit, 'txt_pos_customer_phone')
        self.txt_pos_customer_email = self.findChild(QLineEdit, 'txt_pos_customer_email')
        self.txt_pos_customer_address = self.findChild(QLineEdit, 'txt_pos_customer_address')

    def btn_pos_checkout_click_handler(self):
        """
        method for checking out when all the desired products have been added to the invoice.
        creates an invoice to add into the database containing all the customers information and information
        related to the invoice like time of purchase and items purchased.
        """
        if self.cmb_pos_customer.currentData() in ['select', None]:
            self.lbl_pos_results.setText('Must select a customer to checkout')
        elif len(self.pos_customer_items) == 0:
            self.lbl_pos_results.setText('Cannot checkout an empty invoice')
        else:
            try:
                invoice_total = float(self.lbl_pos_total_price.text().strip("$"))
                customer_id = int(self.cmb_pos_customer.currentData())
                invoice_id = get_max_invoice_id()[0] + 1
                today = date.today()
                sql = f"INSERT INTO `the_athletic_outlet`.`invoices` " \
                      f"(`invoice_id`, `customer_id`, `order_date`, `invoice_total`) " \
                      f"VALUES ('{invoice_id}', '{customer_id}', '{today}', '{invoice_total}');"
                result = execute_query_commit(sql)
                if result == 1:
                    self.lbl_pos_results.setText('Checkout Complete invoice created')
                    for key, value in self.pos_customer_items.items():
                        sql = f"INSERT INTO invoice_line_items VALUES(default, {invoice_id}, {key}, {value['quantity']})"
                        execute_query_commit(sql)
                        stock = get_product_information_by_id(key)['in_stock'] - value['quantity']
                        sql2 = f"UPDATE products SET in_stock = {stock} WHERE product_id = {key};"
                        execute_query_commit(sql2)
                    self.populate_all_tables()
                    self.tbl_pos_invoice.clear()
                    self.txt_pos_customer_email.clear()
                    self.txt_pos_customer_phone.clear()
                    self.txt_pos_customer_address.clear()
                    self.lbl_pos_total_price.clear()
                    self.populate_pos_products_combo_box()
                    self.populate_pos_customers_combo_box()
            except Exception as e:
                self.lbl_pos_results.setText(str(e))

    def btn_pos_add_item_click_handler(self):
        """
        method for adding an item to the invoice.
        grabs info from the cmb_pos_items box and quantity from spb_pos_item_amount and then adds to the invoice.
        """
        if self.cmb_pos_items.currentData() in ['select', None]:
            self.lbl_pos_results.setText('Must select an item to add to inventory')
        else:
            try:
                product_id = self.cmb_pos_items.currentData()
                info = get_product_information_by_id(product_id)
                if product_id in self.pos_customer_items.keys():
                    self.pos_customer_items[product_id]['quantity'] += int(self.spb_pos_item_amount.text())
                else:
                    self.pos_customer_items[product_id] = {'name': info['product_name'], 'vendor': info['vendor'],
                                                           'unit price': info['product_price'],
                                                           'quantity': int(self.spb_pos_item_amount.text())}
                self.populate_pos_invoice()
                self.lbl_pos_results.setText('Item added')
                self.populate_pos_products_combo_box()
            except Exception as e:
                self.lbl_pos_results.setText(str(e))

    def btn_pos_remove_item_click_handler(self):
        """
        method for removing an item from the invoice.
        grabs info from the cmb_pos_items box and the quantity from spb_pos_item_amount then subtracts that amount
        of product from the invoice if possible.
        """
        if self.cmb_pos_items.currentData() in ['select', None]:
            self.lbl_pos_results.setText('Must select an item to remove from inventory')
        else:
            try:
                product_id = self.cmb_pos_items.currentData()
                if product_id in self.pos_customer_items.keys():
                    self.pos_customer_items[product_id]['quantity'] -= int(self.spb_pos_item_amount.text())
                    if self.pos_customer_items[product_id]['quantity'] <= 0:
                        del self.pos_customer_items[product_id]
                    self.lbl_pos_results.setText('Item removed')
                else:
                    self.lbl_pos_results.setText('Item being removed is not part of the invoice')
                self.populate_pos_invoice()
                self.populate_pos_products_combo_box()
            except Exception as e:
                self.lbl_pos_results.setText(str(e))

    def populate_pos_invoice(self):
        """
        for each item in pos_customers_items add its details to a new line
        set lbl_pos_total to the calculated price of all the items
        """
        try:
            self.tbl_pos_invoice.setColumnCount(5)
            self.tbl_pos_invoice.setRowCount(len(self.pos_customer_items))
            self.tbl_pos_invoice.verticalHeader().setVisible(False)
            columns = ['product ID', 'product name', 'vendor', 'unit price', 'quantity']
            self.tbl_pos_invoice.setHorizontalHeaderLabels(columns)
            current_row = 0
            current_price = 0
            for key, value in self.pos_customer_items.items():
                self.tbl_pos_invoice.setItem(current_row, 0, QTableWidgetItem(str(key)))
                self.tbl_pos_invoice.setItem(current_row, 1, QTableWidgetItem(value['name']))
                self.tbl_pos_invoice.setItem(current_row, 2, QTableWidgetItem(value['vendor']))
                self.tbl_pos_invoice.setItem(current_row, 3, QTableWidgetItem(str(value['unit price'])))
                self.tbl_pos_invoice.setItem(current_row, 4, QTableWidgetItem(str(value['quantity'])))
                current_price += (value['quantity'] * value['unit price'])
                current_row += 1
            self.tbl_pos_invoice.resizeColumnsToContents()
            self.tbl_pos_invoice.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            self.lbl_pos_total_price.setText(f"${str(current_price)}")
        except Exception as e:
            self.lbl_pos_results.setText(str(e))

    def populate_pos_products_combo_box(self):
        self.cmb_pos_items.clear()
        rows = get_product_names_and_ids()[1]
        self.cmb_pos_items.addItem('-select-', userData='select')
        for product in rows:
            self.cmb_pos_items.addItem(product[1], userData=product[0])

    def cmb_pos_customer_change_handler(self):
        """
        method for when the index of the cmb_pos_customer box changes.
        grabs information about the customer which will be stored in temp variables to be used when
        the invoice is ready to be completed.
        """
        if self.cmb_pos_customer.currentData() in ['select', None]:
            pass
        else:
            try:
                customer_id = self.cmb_pos_customer.currentData()
                info = get_customer_information_by_id(customer_id)
                self.txt_pos_customer_address.setText(info['address'])
                self.txt_pos_customer_email.setText(info['email'])
                self.txt_pos_customer_phone.setText(info['phone_number'])
            except Exception as e:
                self.lbl_pos_results.setText(str(e))

    def populate_pos_customers_combo_box(self):
        self.cmb_pos_customer.clear()
        rows = get_customer_names_ids()[1]
        self.cmb_pos_customer.addItem('-select-', userData='select')
        for customer in rows:
            self.cmb_pos_customer.addItem(customer[1], userData=customer[0])

    """
    VVVV METHODS FOR THE INVENTORY TAB VVVV
    """

    def initialize_inventory_tab(self):
        """
        initializes all the tabs and widgets on the inventory page.
        """
        self.rdo_inventory_out_of_stock = self.findChild(QRadioButton, 'rdo_inventory_out_of_stock')
        self.rdo_inventory_out_of_stock.toggled.connect(self.rdo_inventory_out_of_stock_change_handler)

        self.tbl_inventory = self.findChild(QTableWidget, 'tbl_inventory')

        self.lbl_inventory_add_results = self.findChild(QLabel, 'lbl_inventory_add_results')
        self.lbl_inventory_update_results = self.findChild(QLabel, 'lbl_inventory_update_results')

        self.txt_inventory_add_product_name = self.findChild(QLineEdit, 'txt_inventory_add_product_name')
        self.txt_inventory_add_description = self.findChild(QLineEdit, 'txt_inventory_add_description')
        self.txt_inventory_add_price = self.findChild(QLineEdit, 'txt_inventory_add_price')
        self.txt_inventory_add_amount = self.findChild(QLineEdit, 'txt_inventory_add_amount')
        self.txt_inventory_update_amount = self.findChild(QLineEdit, 'txt_inventory_update_amount')
        self.txt_inventory_update_description = self.findChild(QLineEdit, 'txt_inventory_update_description')
        self.txt_inventory_update_price = self.findChild(QLineEdit, 'txt_inventory_update_price')
        self.txt_inventory_update_product_id = self.findChild(QLineEdit, 'txt_inventory_update_product_id')
        self.txt_inventory_update_product_name = self.findChild(QLineEdit, 'txt_inventory_update_product_name')
        self.txt_inventory_update_vendor = self.findChild(QLineEdit, 'txt_inventory_update_vendor')

        self.cmb_inventory_update_product = self.findChild(QComboBox, 'cmb_inventory_update_product')
        self.cmb_inventory_update_product.currentIndexChanged.connect(self.cmb_inventory_update_product_change_handler)

        self.cmb_inventory_add_vendor = self.findChild(QComboBox, 'cmb_inventory_add_vendor')

        self.btn_inventory_add_item = self.findChild(QPushButton, 'btn_inventory_add_item')
        self.btn_inventory_add_item.clicked.connect(self.btn_inventory_add_item_click_handler)

        self.btn_inventory_update_product = self.findChild(QPushButton, 'btn_inventory_update_product')
        self.btn_inventory_update_product.clicked.connect(self.btn_inventory_update_product_clicked_handler)

    def rdo_inventory_out_of_stock_change_handler(self):
        """
        method called when the radio button is triggered.
        if the button is checked the tbl_inventory contents will be swapped to show items which have a stock level of 0.
        if the button is unchecked the tbl_inventory will display all inventory items as normal.
        """
        status = self.sender()
        if status.isChecked():
            self.populate_inventory_table_out_of_stock()
        else:
            self.populate_inventory_table_in_stock()

    def cmb_inventory_update_product_change_handler(self):
        """
        method called when the cmb_inventory_update_product index is changed.
        will store the data of the product being updated in the inventory in temp variables using the QLineEdit items
        and vendor combo box allowing the user to make changes.
        """
        if self.cmb_inventory_update_product.currentData() in ['select', None]:
            pass
        else:
            try:
                product_id = self.cmb_inventory_update_product.currentData()
                info = get_product_information_by_id(product_id)
                self.txt_inventory_update_amount.setText(str(info['in_stock']))
                self.txt_inventory_update_description.setText(info['product_description'])
                self.txt_inventory_update_price.setText(str(info['product_price']))
                self.txt_inventory_update_product_id.setText(str(info['product_id']))
                self.txt_inventory_update_product_name.setText(info['product_name'])
                self.txt_inventory_update_vendor.setText(info['vendor'])
            except Exception as e:
                self.lbl_inventory_update_results.setText(e)

    def btn_inventory_add_item_click_handler(self):
        """
        method called when the btn_inventory_add_item is clicked.
        takes the information from the QLineItems and vendor combo box and adds them to the inventory.
        """
        try:
            product_name = self.txt_inventory_add_product_name.text()
            product_description = self.txt_inventory_add_description.text()
            price = float(self.txt_inventory_add_price.text())
            stock = int(self.txt_inventory_add_amount.text())
            vendor = self.cmb_inventory_add_vendor.currentData()
            result = add_product_to_inventory(vendor, product_name, product_description, price, stock)
            if result == 1:
                self.lbl_inventory_add_results.setText('Item added successfully')
                self.txt_inventory_add_price.clear()
                self.txt_inventory_add_description.clear()
                self.txt_inventory_add_amount.clear()
                self.txt_inventory_add_product_name.clear()
                self.populate_inventory_table_in_stock()
                self.populate_inventory_product_combo_box()
        except Exception as e:
            self.lbl_inventory_add_results.setText(str(e))

    def btn_inventory_update_product_clicked_handler(self):
        """
        method called when the btn_inventory_update_product is clicked.
        takes the information from the QLineEdits and vendor combo box and updates the products information in the database
        using the products ID code.
        """
        if self.cmb_inventory_update_product.currentData() in ['select', None]:
            self.lbl_customers_update_results.setText('Must have a product selected to perform an update.')
        else:
            try:
                product_id = int(self.cmb_inventory_update_product.currentData())
                amount = int(self.txt_inventory_update_amount.text())
                description = self.txt_inventory_update_description.text()
                price = float(self.txt_inventory_update_price.text())
                name = self.txt_inventory_update_product_name.text()
                result = update_product_info_using_product_id(product_id, name, description, price, amount)
                if result == 1:
                    self.lbl_inventory_update_results.setText('Product updated')
                    self.populate_inventory_product_combo_box()
                    self.populate_inventory_table_in_stock()
            except Exception as e:
                self.lbl_inventory_update_results.setText(str(e))

    def populate_inventory_table_in_stock(self):
        """
        method for populating the inventory table to show in stock items.
        """
        rows = get_all_inventory_information_in_stock()[1]
        self.populate_table(self.tbl_inventory, rows,
                            ['Product ID', 'Vendor ID', 'Name', 'Description', 'Price', 'Stock'])

    def populate_inventory_table_out_of_stock(self):
        """
        method for populating the inventory table to show items which are out of stock.
        """
        rows = get_all_inventory_information_out_stock()[1]
        self.populate_table(self.tbl_inventory, rows,
                            ['Product ID', 'Vendor ID', 'Name', 'Description', 'Price', 'Stock'])

    def populate_inventory_vendor_combo_boxes(self):
        """
        method for populating/refreshing the vendors combo boxes on the inventory tab.
        """
        self.cmb_inventory_add_vendor.clear()
        rows = get_vendor_names_ids()[1]
        self.cmb_inventory_add_vendor.addItem('-select-', userData='select')
        for vendor in rows:
            self.cmb_inventory_add_vendor.addItem(vendor[1], userData=vendor[0])

    def populate_inventory_product_combo_box(self):
        """
        method for populating and refreshing the inventory_product_combo_box
        """
        self.cmb_inventory_update_product.clear()
        rows = get_product_names_and_ids()[1]
        self.cmb_inventory_update_product.addItem('-select-', userData='select')
        for product in rows:
            self.cmb_inventory_update_product.addItem(product[1], userData=product[0])

    """
    VVVV METHODS FOR THE CUSTOMERS TAB VVVV
    """

    def initialize_customers_tab(self):
        """
        initializes all the tables and widgets on the customers tab
        """
        self.tbl_customers = self.findChild(QTableWidget, 'tbl_customers')
        self.tbl_active_customers = self.findChild(QTableWidget, 'tbl_active_customers')

        self.lbl_customers_new_results = self.findChild(QLabel, 'lbl_customers_new_results')
        self.lbl_customers_update_results = self.findChild(QLabel, 'lbl_customers_update_results')

        self.txt_customers_new_first_name = self.findChild(QLineEdit, 'txt_customers_new_first_name')
        self.txt_customers_new_last_name = self.findChild(QLineEdit, 'txt_customers_new_last_name')
        self.txt_customers_new_phone = self.findChild(QLineEdit, 'txt_customers_new_phone')
        self.txt_customers_new_address = self.findChild(QLineEdit, 'txt_customers_new_address')
        self.txt_customers_new_email = self.findChild(QLineEdit, 'txt_customers_new_email')
        self.txt_customers_update_address = self.findChild(QLineEdit, 'txt_customers_update_address')
        self.txt_customers_update_customer_id = self.findChild(QLineEdit, 'txt_customers_update_customer_id')
        self.txt_customers_update_email = self.findChild(QLineEdit, 'txt_customers_update_email')
        self.txt_customers_update_first_name = self.findChild(QLineEdit, 'txt_customers_update_first_name')
        self.txt_customers_update_last_name = self.findChild(QLineEdit, 'txt_customers_update_last_name')
        self.txt_customers_update_phone_num = self.findChild(QLineEdit, 'txt_customers_update_phone_num')

        self.btn_customers_add_customer = self.findChild(QPushButton, 'btn_customers_add_customer')
        self.btn_customers_add_customer.clicked.connect(self.btn_customers_add_customer_clicked_handler)

        self.btn_customers_update_customer = self.findChild(QPushButton, 'btn_customers_update_customer')
        self.btn_customers_update_customer.clicked.connect(self.btn_customers_update_customer_clicked_handler)

        self.btn_customers_delete_customer = self.findChild(QPushButton, 'btn_customers_delete_customer')
        self.btn_customers_delete_customer.clicked.connect(self.btn_customers_delete_customer_clicked_handler)

        self.cmb_customers_update_customer = self.findChild(QComboBox, 'cmb_customers_update_customer')
        self.cmb_customers_update_customer.currentIndexChanged.connect(
            self.cmb_customers_update_customer_change_handler)

    def btn_customers_add_customer_clicked_handler(self):
        """
        method called when the btn_customers_add_customer is clicked. 
        grabs the info from the QLineEdit items and adds the customer to the database.
        """
        first_name = self.txt_customers_new_first_name.text()
        last_name = self.txt_customers_new_last_name.text()
        phone_num = self.txt_customers_new_phone.text()
        address = self.txt_customers_new_address.text()
        email = self.txt_customers_new_email.text()
        try:
            result = add_customer(first_name, last_name, phone_num, email, address)
            if result == 1:
                self.lbl_customers_new_results.setText('Customer added')
                self.txt_customers_new_address.clear()
                self.txt_customers_new_email.clear()
                self.txt_customers_new_first_name.clear()
                self.txt_customers_new_last_name.clear()
                self.txt_customers_new_phone.clear()
                self.populate_update_customers_cmb_box()
                self.populate_customer_table()
                self.populate_active_customers_table()
        except Exception as e:
            self.lbl_customers_new_results.setText(str(e))

    def btn_customers_delete_customer_clicked_handler(self):
        """
        method called when the btn_customers_delete_customer is clicked.
        using the customer id store in the QLineEdit will delete the customer from the database.
        """
        if self.cmb_customers_update_customer.currentData() in ['select', None]:
            self.lbl_customers_update_results.setText('Must have a customer selected to perform an update or delete.')
        else:
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Delete Confirmation")
                msg.setText(f"Are you sure you want to delete {self.txt_customers_update_first_name.text()} "
                            f"{self.txt_customers_update_last_name.text()}? this will also delete all invoices belonging to this "
                            f"customer.")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                msg.setIcon(QMessageBox.Icon.Question)
                button = msg.exec()
                if button == QMessageBox.StandardButton.Yes:
                    customer_id = int(self.txt_customers_update_customer_id.text())
                    result = delete_customer_by_id(customer_id)
                    if result == 1:
                        self.lbl_customers_update_results.setText('Customer Deleted')
                        self.txt_customers_update_address.clear()
                        self.txt_customers_update_customer_id.clear()
                        self.txt_customers_update_email.clear()
                        self.txt_customers_update_first_name.clear()
                        self.txt_customers_update_last_name.clear()
                        self.txt_customers_update_phone_num.clear()
                        self.populate_update_customers_cmb_box()
                        self.populate_all_tables()
            except Exception as e:
                self.lbl_customers_update_results.setText(str(e))

    def btn_customers_update_customer_clicked_handler(self):
        """
        method called when the btn_customers_update_customer is clicked.
        using the customer id and the info from the QLineEdits will update the customers information in the database.
        """
        if self.cmb_customers_update_customer.currentData() in ['select', None]:
            self.lbl_customers_update_results.setText('Must have a customer selected to perform an update or delete.')
        else:
            try:
                customer_id = int(self.txt_customers_update_customer_id.text())
                address = self.txt_customers_update_address.text()
                email = self.txt_customers_update_email.text()
                first_name = self.txt_customers_update_first_name.text()
                last_name = self.txt_customers_update_last_name.text()
                phone_num = self.txt_customers_update_phone_num.text()
                result = update_customer_by_id(customer_id, first_name, last_name, phone_num, email, address)
                if result == 1:
                    self.lbl_customers_update_results.setText('Customer information updated')
                    self.txt_customers_update_address.clear()
                    self.txt_customers_update_customer_id.clear()
                    self.txt_customers_update_email.clear()
                    self.txt_customers_update_first_name.clear()
                    self.txt_customers_update_last_name.clear()
                    self.txt_customers_update_phone_num.clear()
                    self.populate_update_customers_cmb_box()
                    self.populate_all_tables()
            except Exception as e:
                self.lbl_customers_update_results.setTest(str(e))

    def cmb_customers_update_customer_change_handler(self):
        """
        method called when the cmb_customers_update_customer combo box's inde is changed.
        grabs the info on the new customer from the database stores in temporary variables using the QLineEdit items.
        """
        if self.cmb_customers_update_customer.currentData() in ['select', None]:
            pass
        else:
            try:
                customer_id = self.cmb_customers_update_customer.currentData()
                info = get_customer_information_by_id(customer_id)
                self.txt_customers_update_address.setText(info['address'])
                self.txt_customers_update_customer_id.setText(str(info['customer_id']))
                self.txt_customers_update_email.setText(info['email'])
                self.txt_customers_update_first_name.setText(info['first_name'])
                self.txt_customers_update_last_name.setText(info['last_name'])
                self.txt_customers_update_phone_num.setText(info['phone_number'])
            except Exception as e:
                self.lbl_customers_update_results.setText(str(e))

    def populate_update_customers_cmb_box(self):
        """
        method for populating/refreshing the update_customer_cmb_box
        """
        self.cmb_customers_update_customer.clear()
        rows = get_customer_names_ids()[1]
        self.cmb_customers_update_customer.addItem('-select-', userData='select')
        for customer in rows:
            self.cmb_customers_update_customer.addItem(customer[1], userData=customer[0])

    def populate_customer_table(self):
        """
        method called to populate/refresh the customer table on the customers tab.
        """
        rows = get_all_customer_information()[1]
        self.populate_table(self.tbl_customers, rows,
                            ['ID', 'First Name', 'Last Name', 'Phone Num', 'Email', 'Address'])

    def populate_active_customers_table(self):
        """
        method called to populate/refresh the active customer table on the customers tab.
        """
        rows = get_active_customers()[1]
        self.populate_table(self.tbl_active_customers, rows,
                            ['ID', 'First Name', 'Last Name', 'Phone Num', 'Email', 'Address'])

    """
    VVVV METHODS FOR THE INVOICES TAB VVVV
    """

    def initialize_invoices_tab(self):
        """
        initializes all the tables and widgets on the invoices tab.
        """
        self.tbl_invoices = self.findChild(QTableWidget, 'tbl_invoices')
        self.tbl_invoices_items_purchased = self.findChild(QTableWidget, 'tbl_invoices_items_purchased')

        self.txt_invoices_invoice_num = self.findChild(QLineEdit, 'txt_invoices_invoice_num')
        self.txt_invoices_address = self.findChild(QLineEdit, 'txt_invoices_address')
        self.txt_invoices_customer_id = self.findChild(QLineEdit, 'txt_invoices_customer_id')
        self.txt_invoices_customer_name = self.findChild(QLineEdit, 'txt_invoices_customer_name')
        self.txt_invoices_date = self.findChild(QLineEdit, 'txt_invoices_date')
        self.txt_invoices_email = self.findChild(QLineEdit, 'txt_invoices_email')
        self.txt_invoices_phone_num = self.findChild(QLineEdit, 'txt_invoices_phone_num')

        self.btn_invoices_view_details = self.findChild(QPushButton, 'btn_invoices_view_details')
        self.btn_invoices_view_details.clicked.connect(self.btn_invoices_view_details_click_handler)

        self.btn_invoices_delete_invoice = self.findChild(QPushButton, 'btn_invoices_delete_invoice')
        self.btn_invoices_delete_invoice.clicked.connect(self.btn_invoices_delete_invoice_clicked_handler)

    def btn_invoices_view_details_click_handler(self):
        """
        method called when the btn_invoices_view_details is clicked.
        uses the invoice id from the txt_invoices_invoice_num to display the details of the invoice 
        in the QLineEdit items on the invoice page and gets the information
        of the items belonging to the invoice and displays in the tbl_invoices_items_purchased.
        """
        try:
            invoice_id = int(self.txt_invoices_invoice_num.text())
            invoice_info = get_invoice_information_by_id(invoice_id)
            self.txt_invoices_address.setText(invoice_info['address'])
            self.txt_invoices_customer_id.setText(str(invoice_info['customer_id']))
            self.txt_invoices_customer_name.setText(invoice_info['name'])
            self.txt_invoices_email.setText(invoice_info['email'])
            self.txt_invoices_phone_num.setText(invoice_info['phone_number'])
            self.txt_invoices_date.setText(invoice_info['date'])
            self.populate_invoices_items_table()
        except IndexError:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("Invoice Number does not exist")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except ValueError:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("Invoice Number must be an integer value")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(type(e))
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def btn_invoices_delete_invoice_clicked_handler(self):
        """
        method called when the btn_invoices_delete_invoice is clicked.
        uses the invoice number from the txt_invoices_invoice_num to delete the invoice from database.
        """
        try:
            invoice_id = int(self.txt_invoices_invoice_num.text())
            msg = QMessageBox(self)
            msg.setWindowTitle("Delete Confirmation")
            msg.setText(f"Are you sure you want to delete invoice {invoice_id}? this cannot be undone.")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setIcon(QMessageBox.Icon.Question)
            button = msg.exec()
            if button == QMessageBox.StandardButton.Yes:
                delete_invoice_by_id(invoice_id)
                self.txt_invoices_address.clear()
                self.txt_invoices_customer_id.clear()
                self.txt_invoices_customer_name.clear()
                self.txt_invoices_email.clear()
                self.txt_invoices_phone_num.clear()
                self.txt_invoices_date.clear()
                self.tbl_invoices_items_purchased.clear()
                self.populate_invoices_table()
        except IndexError:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("Invoice Number does not exist")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except ValueError:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("Invoice Number must be an integer value")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(type(e))
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def populate_invoices_table(self):
        """
        method called to populate the invoices table on the invoices tab
        """
        rows = get_all_invoice_information()[1]
        self.populate_table(self.tbl_invoices, rows, ['Invoice Number', 'Customer ID', 'Customer', 'Date', 'Total'])

    def populate_invoices_items_table(self):
        """
        method called when you want to view the items belonging to an invoice
        """
        invoice_id = int(self.txt_invoices_invoice_num.text())
        rows = get_invoice_items_by_invoice_id(invoice_id)[1]
        self.populate_table(self.tbl_invoices_items_purchased, rows,
                            ['Product ID', 'Product', 'Unit Price', 'Purchased'])

    """
    VVVV MORE GENERIC USEFUL METHODS VVVV
    """

    def populate_table(self, table, rows, columns):
        """
        Refreshes a table with new data.
        :PARAM:
            table: QTableWidget: The QTableWidget object to refresh.
            rows: list: A list of lists, where each sub-list contains the data for a row in the table.
            columns: list: A list of strings, where each string represents the name of a column in the table.
        """
        table.setRowCount(len(rows))
        table.setColumnCount(len(columns))
        for i in range(len(rows)):
            row = rows[i]
            for j in range(len(row)):
                table.setItem(i, j, QTableWidgetItem(str(row[j])))
        for i in range(table.columnCount()):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))
        table.verticalHeader().setVisible(False)
        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(len(columns) - 1, QHeaderView.ResizeMode.Stretch)

    def populate_all_tables(self):
        """
        method for populating/ refreshing all the tables in the gui. Use when app is first loaded or when
        large changes are made that affect all tables.
        """
        self.populate_customer_table()
        self.populate_active_customers_table()
        self.populate_inventory_table_in_stock()
        self.populate_invoices_table()

    def populate_all_combo_boxes(self):
        """
        method for refreshing all combo boxes in the gui. use when app is first loaded or when an update is performed
        on data being used in the combo box.
        """
        self.populate_update_customers_cmb_box()
        self.populate_inventory_vendor_combo_boxes()
        self.populate_inventory_product_combo_box()
        self.populate_pos_products_combo_box()
        self.populate_pos_customers_combo_box()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
