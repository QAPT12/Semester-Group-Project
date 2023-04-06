from PyQt6 import uic
from PyQt6.QtWidgets import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)

        self.initialize_pos_tab()

        self.initialize_inventory_tab()

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

        self.btn_inventory_add_item = self.findChild(QPushButton, 'btn_inventory_add_item')
        self.btn_inventory_add_item.clicked.connect(self.btn_inventory_add_item_click_handler)

        self.btn_inventory_update_product = self.findChild(QPushButton, 'btn_inventory_update_product')
        self.btn_inventory_delete_product = self.findChild(QPushButton, 'btn_inventory_delete_product')

    def rdo_inventory_out_of_stock_change_handler(self):
        status = self.sender()
        if status.isChecked():
            print('out of stock button checked')
        else:
            print('out of stock button unchecked')

    def cmb_inventory_update_product_change_handler(self):
        print('product changed')

    def btn_inventory_add_item_click_handler(self):
        print('item added to inventory')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
