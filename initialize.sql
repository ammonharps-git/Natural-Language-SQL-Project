
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

INSERT INTO Customers (name, email, phone) VALUES
('Alice Johnson', 'alice.johnson@example.com', '555-1234'),
('Bob Smith', 'bob.smith@example.com', '555-5678'),
('Charlie Brown', 'charlie.brown@example.com', '555-8765'),
('Diana Prince', 'diana.prince@example.com', '555-4321'),
('Ethan Hunt', 'ethan.hunt@example.com', '555-2468'),
('Joseph Stalin', 'joe.stalin@example.com', '555-5454'),
('Sam Snapneck', 'sam.snapneck@example.com', '555-8888');

INSERT INTO Orders (customer_id, order_date, total_amount) VALUES
(1, '2024-10-01', 29.99),
(1, '2024-10-02', 45.50),
(2, '2024-10-01', 15.75),
(3, '2024-10-03', 32.00),
(4, '2024-10-01', 50.00),
(5, '2024-10-04', 22.25),
(2, '2024-10-03', 27.30),
(6, '2024-10-01', 100.32),
(6, '2024-10-01', 54.23),
(7, '2024-10-05', 1.25);