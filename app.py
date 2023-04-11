from PyQt6 import uic
from PyQt6.QtWidgets import *
import sys
from controller import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)

        self.initialize_pos_tab()

        self.initialize_inventory_tab()
        
        self.initialize_customers_tab()

        self.initialize_invoices_tab()

        self.populate_all_tables()

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
        self.cmb_pos_items.currentIndexChanged.connect(self.cmb_pos_items_change_handler)

        self.cmb_pos_customer = self.findChild(QComboBox, 'cmb_pos_customer')
        self.cmb_pos_customer.currentIndexChanged.connect(self.cmb_pos_customer_change_handler)

        self.spb_pos_item_amount = self.findChild(QSpinBox, 'spb_pos_item_amount')

        self.txt_pos_customer_phone = self.findChild(QLineEdit, 'txt_pos_customer_phone')
        self.txt_pos_customer_email = self.findChild(QLineEdit, 'txt_pos_customer_email')
        self.txt_customer_address = self.findChild(QLineEdit, 'txt_customer_address')


    def btn_pos_checkout_click_handler(self):
        """
        method for checking out when all the desired products have been added to the invoice.
        creates an invoice to add into the database containing all the customers information and information
        related to the invoice like time of purchase and items purchased.
        """
        print('checkout')

    def btn_pos_add_item_click_handler(self):
        """
        method for adding an item to the invoice.
        grabs info from the cmb_pos_items box and quantity from spb_pos_item_amount and then adds to the invoice.
        """
        print('add item')

    def btn_pos_remove_item_click_handler(self):
        """
        method for removing an item from the invoice.
        grabs info from the cmb_pos_items box and the quantity from spb_pos_item_amount then subtracts that amount
        of product from the invoice if possible.
        """
        print('remove item')

    def cmb_pos_items_change_handler(self):
        """
        method called when the index of the cmb_pos_items box changes.
        will simply grab the information about the item from the database and store it into temp variables which
        can be used by the prior methods for adding and removing from invoice.
        """
        print('item change')

    def cmb_pos_customer_change_handler(self):
        """
        method for when the index of the cmb_pos_customer box changes.
        grabs information about the customer which will be stored in temp variables to be used when
        the invoice is ready to be completed.
        """
        print('customer change')

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
        self.txt_inventory_product_id = self.findChild(QLineEdit, 'txt_inventory_product_id')
        self.txt_inventory_update_product_name = self.findChild(QLineEdit, 'txt_inventory_update_product_name')

        self.cmb_inventory_update_product = self.findChild(QComboBox, 'cmb_inventory_update_product')
        self.cmb_inventory_update_product.currentIndexChanged.connect(self.cmb_inventory_update_product_change_handler)

        self.cmb_inventory_update_vendor = self.findChild(QComboBox, 'cmb_inventory_update_vendor')
        self.cmb_inventory_add_vendor = self.findChild(QComboBox, 'cmb_inventory_add_vendor')
        
        self.btn_inventory_add_item = self.findChild(QPushButton, 'btn_inventory_add_item')
        self.btn_inventory_add_item.clicked.connect(self.btn_inventory_add_item_click_handler)

        self.btn_inventory_update_product = self.findChild(QPushButton, 'btn_inventory_update_product')
        self.btn_inventory_update_product.clicked.connect(self.btn_inventory_update_product_clicked_handler)

        self.btn_inventory_delete_product = self.findChild(QPushButton, 'btn_inventory_delete_product')
        self.btn_inventory_delete_product.clicked.connect(self.btn_inventory_delete_product_clicked_handler)

    def rdo_inventory_out_of_stock_change_handler(self):
        """
        method called when the radio button is triggered.
        if the button is checked the tbl_inventory contents will be swapped to show items which have a stock level of 0.
        if the button i unchecked the tbl_inventory will display all invneotry items as normal.
        """
        status = self.sender()
        if status.isChecked():
            print('out of stock button checked')
        else:
            print('out of stock button unchecked')

    def cmb_inventory_update_product_change_handler(self):
        """
        method called when the cmb_inventory_update_product index is changed.
        will store the data of the product being updated in the inventory in temp variables using the QLineEdit items
        and vendor combo box allowing the user to make changes.
        """
        print('product changed')

    def btn_inventory_add_item_click_handler(self):
        """
        method called when the btn_inventory_add_item is clicked.
        takes the information from the QLineItems and vendor combo box and adds them to the inventory.
        """
        print('item added to inventory')

    def btn_inventory_update_product_clicked_handler(self):
        """
        method called when the btn_inventory_update_product is clicked.
        takes the information from the QLineEdits and vendor combo box and updates the products information in the database
        using the products ID code.
        """
        print('item updated in inventory')

    def btn_inventory_delete_product_clicked_handler(self):
        """
        method called then the btn_inventory_delete_product is clicked.
        using the temp data and product id from the cmb_inventory_product_update combo box
        """
        print('item deleted from inventory')

    def initialize_customers_tab(self):
        """
        initializes all the tables and widgets on the customers tab
        """
        self.tbl_customers = self.findChild(QTableWidget, 'tbl_customers')
        self.tbl_active_customers = self.findChild(QTableWidget, 'tbl_active_customers')

        self.lbl_customers_new_results = self.findChild(QLabel, 'lbl_customers_new_results')
        self.lbl_customers_update_results = self.findChild(QLabel, 'lbl_customers_update_results')

        self.txt_customers_new_first_name = self.findChild(QTableWidget, 'txt_customers_new_first_name')
        self.txt_customers_new_last_name = self.findChild(QTableWidget, 'txt_customers_new_last_name')
        self.txt_customers_new_phone = self.findChild(QTableWidget, 'txt_customers_new_phone')
        self.txt_customers_new_address = self.findChild(QTableWidget, 'txt_customers_new_address')
        self.txt_customers_new_email = self.findChild(QTableWidget, 'txt_customers_new_email')
        self.txt_customers_update_address = self.findChild(QTableWidget, 'txt_customers_update_address')
        self.txt_customers_update_customer_id = self.findChild(QTableWidget, 'txt_customers_update_customer_id')
        self.txt_customers_update_email = self.findChild(QTableWidget, 'txt_customers_update_email')
        self.txt_customers_update_first_name = self.findChild(QTableWidget, 'txt_customers_update_first_name')
        self.txt_customers_update_last_name = self.findChild(QTableWidget, 'txt_customers_update_last_name')
        self.txt_customers_update_phone_num = self.findChild(QTableWidget, 'txt_customers_update_phone_num')

        self.btn_customers_add_customer = self.findChild(QPushButton, 'btn_customers_add_customer')
        self.btn_customers_add_customer.clicked.connect(self.btn_customers_add_customer_clicked_handler)

        self.btn_customers_update_customer = self.findChild(QPushButton, 'btn_customers_update_customer')
        self.btn_customers_update_customer.clicked.connect(self.btn_customers_update_customer_clicked_handler)

        self.btn_customers_delete_customer = self.findChild(QPushButton, 'btn_customers_delete_customer')
        self.btn_customers_delete_customer.clicked.connect(self.btn_customers_delete_customer_clicked_handler)

        self.cmb_customers_update_customer = self.findChild(QComboBox, 'cmb_customers_update_customer')
        self.cmb_customers_update_customer.currentIndexChanged.connect(self.cmb_customers_update_customer_change_handler)
        
    def btn_customers_add_customer_clicked_handler(self):
        """
        method called when the btn_customers_add_customer is clicked. 
        grabs the info from the QLineEdit items and adds the customer to the database.
        """
        print('customer added')

    def btn_customers_delete_customer_clicked_handler(self):
        """
        method called when the btn_customers_delete_customer is clicked.
        using the customer id store in the QLineEdit will delete the customer from the database.
        """
        print('customer deleted')

    def btn_customers_update_customer_clicked_handler(self):
        """
        method called when the btn_customers_update_customer is clicked.
        using the customer id and the info from the QLineEdits will update the customers information in the database.
        """
        print('customer updated')

    def cmb_customers_update_customer_change_handler(self):
        """
        method called when the cmb_customers_update_customer combo box's inde is changed.
        grabs the info on the new customer from the database stores in temporary variables using the QLineEdit items.
        """
        print('customer changed')

    def populate_customer_table(self):
        """
        method called to populate/refresh the customer table on the customers tab.
        """
        self.tbl_customers.setColumnCount(6)
        self.tbl_customers.verticalHeader().setVisible(False)
        self.tbl_customers.setHorizontalHeaderLabels(['ID', 'First Name', 'Last Name', 'Phone Num.', 'Email', 'Address'])
        customers_info = get_all_customer_information()[1]
        self.tbl_customers.setRowCount(len(customers_info))
        for i in range(len(customers_info)):
            row = customers_info[i]
            for j in range(len(row)):
                self.tbl_customers.setItem(i, j, QTableWidgetItem(str(row[j])))
        self.tbl_customers.resizeColumnsToContents()
        self.tbl_customers.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

    def populate_active_customers_table(self):
        """
        method called to populate.refresh the active customer table on the customers tab.
        """
        self.tbl_active_customers.setColumnCount(4)

    def initialize_invoices_tab(self):
        """
        initrializes all the tables and widgets on the invoices tab.
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
        of the items belonging to the invoice and disaplys in the tbl_invoices_items_purchased.
        """
        print('invoice details')

    def btn_invoices_delete_invoice_clicked_handler(self):
        """
        method called when the btn_invoices_delete_invoice is clicked.
        uses the invoice number from the txt_invoices_invoice_num to delete the invoice from database.
        """
        print('invoice deleted')

    def populate_all_tables(self):
        """
        method for populating/ refreshing all the tables in the gui. Use when app is first loaded or when
        large changes are made that affect all tables.
        """
        self.populate_customer_table()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
