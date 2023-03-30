from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QLabel, QPushButton

from sql import db, cursor


class NewClientWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setModal(True)

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(QLabel("ФИО клиента:"))
        self.new_client_name = QtWidgets.QLineEdit(self.parent.client_name_input.text())
        layout.addWidget(self.new_client_name)

        layout.addWidget(QLabel("Номер телефона клиента:"))
        self.client_phone_number_input = QtWidgets.QLineEdit()
        layout.addWidget(self.client_phone_number_input)

        layout.addWidget(QLabel("Электронная почта клиента:"))
        self.client_email_input = QtWidgets.QLineEdit()
        layout.addWidget(self.client_email_input)

        self.create_client_button = QPushButton("Добавить клиента")
        layout.addWidget(self.create_client_button)
        self.create_client_button.clicked.connect(self.create_client)

        self.setLayout(layout)

    def create_client(self):
        client_name = self.new_client_name.text()
        if not client_name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите имя клиента")
            return

        phone_number = self.client_phone_number_input.text().lstrip("+")
        if len(phone_number) != 11 or not (
            phone_number.startswith("7") or phone_number.startswith("8")
        ):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный номер телефона")
            return

        email = self.client_email_input.text()
        if "@" not in email:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный почтовый адрес")
            return

        cursor.execute(
            "INSERT INTO clients (full_name, phone, email) VALUES (%s, %s, %s)",
            (client_name, phone_number, email),
        )

        db.commit()

        QtWidgets.QMessageBox.information(self, "Успех", "Клиент создан")
        self.close()
