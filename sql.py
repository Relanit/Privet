import mysql.connector

db = mysql.connector.connect(
    host="localhost", user="root", password="1234", database="otk"
)

cursor = db.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS services (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE NOT NULL, cost DECIMAL(10, 2) NOT NULL)"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS clients (id INT AUTO_INCREMENT PRIMARY KEY, full_name VARCHAR(255) NOT NULL, phone VARCHAR(20) NOT NULL, email VARCHAR(255) NOT NULL)"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, client_name VARCHAR(255) NOT NULL, lab_vessel_code INT NOT NULL, services MEDIUMTEXT NOT NULL, total_cost DECIMAL(10, 2) NOT NULL)"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS lab_vessels (id INT AUTO_INCREMENT PRIMARY KEY, vessel_name VARCHAR(255))"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, login VARCHAR(255) UNIQUE, password VARCHAR(255))"
)

db.commit()


# sql = "INSERT INTO services (name, cost) VALUES (%s, %s)"
# val = [
#     ("Бухгалтерские услуги", 1000.00),
#     ("Услуги по управлению закупками", 1500.00),
#     ("Услуги по управлению поставками", 2000.00),
#     ("Услуги по контролю качества", 2500.00),
#     ("Услуги технического контроля", 3000.00),
# ]
#
# cursor.executemany(sql, val)
# db.commit()

# sql = "INSERT INTO lab_vessels (vessel_name) VALUES (%s)"
# values = [("Мензурка ",), ("Колба ",), ("Пробирка",), ("Чашка Петри",)]
# cursor.executemany(sql, values)
# db.commit()