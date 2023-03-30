import traceback

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
)

from personal_window.admin_window.new_order_window.new_client_window import (
    NewClientWindow,
)

from sql import db, cursor


class NewOrderWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setCentralWidget(QWidget())

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        self.centralWidget().setLayout(layout)

        layout.addWidget(QLabel("Код лабораторного сосуда:"))

        self.lab_vessel_code_input = QLineEdit()
        layout.addWidget(self.lab_vessel_code_input)

        layout.addWidget(QLabel("ФИО клиента:"))
        self.client_name_input = QtWidgets.QLineEdit()
        layout.addWidget(self.client_name_input)

        cursor.execute("SELECT * FROM services")
        services = cursor.fetchall()
        costs = {service[1]: int(service[2]) for service in services}

        self.services_checkboxes = []
        for service in services:
            checkbox = QCheckBox(service[1])
            self.services_checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        buttons_box = QGroupBox()
        buttons_layout = QHBoxLayout()
        buttons_box.setLayout(buttons_layout)

        self.save_order_button = QPushButton("Сформировать заказ")
        buttons_layout.addWidget(self.save_order_button)
        self.save_order_button.clicked.connect(lambda: self.save_order(costs))

        self.to_personal_button = QPushButton("Назад")
        buttons_layout.addWidget(self.to_personal_button)
        self.to_personal_button.clicked.connect(self.to_personal)

        layout.addWidget(buttons_box)

    def save_order(self, costs):
        lab_vessel_code = self.lab_vessel_code_input.text()
        if not lab_vessel_code:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Введите код лаборантского сосуда"
            )
            return

        try:
            lab_vessel_code = int(lab_vessel_code)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Код лаборантского сосуда должен быть числом"
            )
            return

        cursor.execute(f"SELECT * FROM lab_vessels WHERE id = {lab_vessel_code}")
        lab_vessel = cursor.fetchone()

        if not lab_vessel:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Лаборантский сосуд с таким кодом не найден"
            )
            return

        client_name = self.client_name_input.text()
        if not client_name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите имя клиента")
            return

        cursor.execute(
            f"SELECT * FROM clients WHERE LOWER(full_name) = LOWER('{client_name}')"
        )
        client = cursor.fetchone()

        if not client:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Клиент с таким именем не найден, создайте нового."
            )
            self.new_client_modal = NewClientWindow(self)
            self.new_client_modal.setWindowTitle("Создание клиента")
            self.new_client_modal.show()
            return

        client_name = client[1]

        total_cost = 0

        service_names = []

        for checkbox in self.services_checkboxes:
            if checkbox.isChecked():
                service_names.append(checkbox.text())
                total_cost += costs[checkbox.text()]

        if not service_names:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите услуги")
            return

        service_names = ", ".join(service_names)

        cursor.execute(
            "INSERT INTO orders (client_name, lab_vessel_code, services, total_cost, checked) VALUES (%s, %s, %s, %s, %s)",
            (client_name, lab_vessel_code, service_names, total_cost, 0),
        )
        db.commit()

        QtWidgets.QMessageBox.information(self, "Успех", "Заказ сформирован")

        self.lab_vessel_code_input.setText("")
        self.client_name_input.setText("")

        for checkbox in self.services_checkboxes:
            if checkbox.isChecked():
                checkbox.setChecked(False)

    def to_personal(self):
        self.deleteLater()
        self.parent.to_personal()
