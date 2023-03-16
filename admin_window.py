from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton, QGroupBox, )

from sql import cursor


class AdminWindow(QMainWindow):
    def __init__(self, parent, login):
        super().__init__()

        self.parent = parent
        self.setCentralWidget(QWidget())
        self.login = login

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.centralWidget().setLayout(layout)

        cursor.execute(f"SELECT * FROM users WHERE login = '{self.login}'")
        user = cursor.fetchone()

        layout.addWidget(QLabel("Информация об аккаунте:"))
        layout.addWidget(QLabel(f"id: {user[0]}"))
        layout.addWidget(QLabel(f"Логин: {self.login}"))
        layout.addWidget(QLabel(f"Пароль: {user[2]}"))

        buttons_box = QGroupBox()
        buttons_layout = QGridLayout()
        buttons_box.setLayout(buttons_layout)


        self.logout_button = QPushButton("Выйти из акаунта")
        buttons_layout.addWidget(self.logout_button, 0, 0)
        self.logout_button.clicked.connect(self.log_out)

        self.create_order_button = QPushButton("Сформировать заказ")
        buttons_layout.addWidget(self.create_order_button, 0, 1)
        self.create_order_button.clicked.connect(self.new_order)

        self.view_orders_button = QPushButton("Список заказов")
        buttons_layout.addWidget(self.view_orders_button, 1, 0)
        self.view_orders_button.clicked.connect(self.view_orders)

        self.view_clients_button = QPushButton("Список клиентов")
        buttons_layout.addWidget(self.view_clients_button, 1, 1)
        self.view_clients_button.clicked.connect(self.view_clients)

        self.view_vessels_button = QPushButton("Список лабораторных сосудов")
        buttons_layout.addWidget(self.view_vessels_button, 2, 0)
        self.view_vessels_button.clicked.connect(self.view_vessels)

        self.create_service_button = QPushButton("Создание услуги")
        buttons_layout.addWidget(self.create_service_button, 2, 1)
        self.create_service_button.clicked.connect(self.new_service)

        layout.addWidget(buttons_box)

    def log_out(self):
        QtWidgets.QMessageBox.information(self, "Успех", "Вы вышли из аккаунта")
        self.parent.to_login()

    def new_order(self):
        self.parent.to_new_order()

    def view_orders(self):
        self.parent.to_view_orders()

    def view_clients(self):
        self.parent.to_view_clients()

    def view_vessels(self):
        self.parent.to_view_vessels()

    def new_service(self):
        self.parent.to_new_service()
