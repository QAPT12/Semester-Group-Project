DROP DATABASE IF EXISTS the_athletic_outlet;
CREATE DATABASE the_athletic_outlet;

USE the_athletic_outlet;

CREATE TABLE customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone_number VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  home_address VARCHAR(50) NOT NULL
);

CREATE TABLE vendors (
  vendor_id INT AUTO_INCREMENT PRIMARY KEY,
  vendor_name VARCHAR(50) NOT NULL
);

CREATE TABLE products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  vendor_id INT NOT NULL,
  product_name VARCHAR(50) NOT NULL,
  product_description VARCHAR(200) NOT NULL,
  product_price DECIMAL(10, 2) NOT NULL,
  in_stock INT NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE invoices (
  invoice_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  order_date DATE NOT NULL,
  ship_amount DECIMAL(10, 2) NOT NULL,
  tax_amount DECIMAL(10, 2) NOT NULL,
  shipping_address VARCHAR(50) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE invoice_line_items (
	item_id INT PRIMARY KEY,
	invoice_id INT NOT NULL,
    product_id INT NOT NULL,
    line_item_amount DECIMAL(10, 2) NOT NULL,
    line_item_description VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
	FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
	);

INSERT INTO customers (first_name, last_name, phone_number, email, home_address)
VALUES ('John', 'Doe', '123-456-7890', 'johndoe@example.com', '123 Main St'),
('Jane', 'Smith', '555-555-5555', 'janesmith@example.com', '456 Elm St'),
('Bob', 'Johnson', '987-654-3210', 'bobjohnson@example.com', '789 Oak St');

INSERT INTO vendors (vendor_name)
VALUES ('Nike'),
('Adidas'),
('Under Armour');

INSERT INTO products (vendor_id, product_name, product_description, product_price, in_stock)
VALUES (1, 'Air Max 90', 'Classic Nike sneakers', 100.00, 50),
(1, 'Dry Fit T-Shirt', 'Moisture-wicking workout shirt', 25.00, 100),
(2, 'Ultraboost 21', 'Comfortable Adidas running shoes', 150.00, 75),
(2, 'Sweatpants', 'Comfortable and stylish pants', 50.00, 50),
(3, 'HeatGear Armour', 'Under Armour compression shirt', 30.00, 150),
(3, 'Recover Sleepwear', 'UAs specialized sleepwear', 60.00, 25),
(1, 'Hockey Helmet', 'Wayne Gretzky Signiture Helmet', 99.99, 0);

INSERT INTO invoices (customer_id, order_date, ship_amount, tax_amount, shipping_address)
VALUES (1, '2023-04-08', 10.00, 7.50, '123 Main St'),
(2, '2023-04-07', 5.00, 3.75, '456 Elm St'),
(3, '2023-04-05', 7.50, 5.63, '789 Oak St');

INSERT INTO invoice_line_items (item_id, invoice_id, product_id, line_item_amount, line_item_description, quantity)
VALUES (1, 1, 1, 100.00, 'Air Max 90 size 10', 1),
(2, 1, 2, 25.00, 'Dry Fit T-Shirt size M', 2),
(3, 2, 3, 150.00, 'Ultraboost 21 size 9', 1),
(4, 2, 4, 50.00, 'Sweatpants size L', 1),
(5, 3, 5, 30.00, 'HeatGear Armour size S', 3),
(6, 3, 6, 60.00, 'Recover Sleepwear size M', 1)