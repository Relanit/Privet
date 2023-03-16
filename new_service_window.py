import traceback

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
)

from sql import db, cursor


class NewServiceWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setCentralWidget(QWidget())

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.centralWidget().setLayout(layout)

        layout.addWidget(QLabel("Название:"))

        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Стоимость:"))
        self.cost_input = QtWidgets.QLineEdit()
        layout.addWidget(self.cost_input)

        buttons_box = QGroupBox()
        buttons_layout = QHBoxLayout()
        buttons_box.setLayout(buttons_layout)

        self.save_service_button = QPushButton("Создать услугу")
        buttons_layout.addWidget(self.save_service_button)
        self.save_service_button.clicked.connect(self.save_service)

        self.to_admin_button = QPushButton("Назад")
        buttons_layout.addWidget(self.to_admin_button)
        self.to_admin_button.clicked.connect(self.to_admin)

        layout.addWidget(buttons_box)

    def save_service(self):
        name = self.name_input.text()
        if not name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите имя услуги")
            return

        try:
            cost = int(self.cost_input.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Стоимость услуги должна быть числом"
            )
            return

        if not cost:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите стоимость услуги")
            return

        try:

            cursor.execute(f"SELECT * FROM services WHERE LOWER(name) = LOWER('{name}')")
            if service := cursor.fetchone():
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Такая услуга уже есть")
                return

            cursor.execute(
                "INSERT INTO services (name, cost) VALUES (%s, %s)",
                (name, float(cost)),
            )
            db.commit()

            QtWidgets.QMessageBox.information(self, "Успех", "Услуга добавлена")

            self.name_input.setText("")
            self.cost_input.setText("")
        except:
            traceback.print_exc()

    def to_admin(self):
        self.deleteLater()
        self.parent.to_admin()
