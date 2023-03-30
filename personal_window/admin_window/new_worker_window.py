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
    QVBoxLayout,
    QHBoxLayout,
)

from sql import db, cursor


class NewWorkerWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setCentralWidget(QWidget())
        self.centralWidget()

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.centralWidget().setLayout(layout)

        group_inputs_box = QGroupBox()
        group_inputs_layout = QVBoxLayout()
        group_inputs_box.setLayout(group_inputs_layout)

        group_inputs_layout.addWidget(QLabel("Логин:"))
        self.login = QLineEdit()
        group_inputs_layout.addWidget(self.login)

        group_inputs_layout.addWidget(QLabel("Пароль:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        group_inputs_layout.addWidget(self.password)

        layout.addWidget(group_inputs_box)

        buttons_box = QGroupBox()
        buttons_layout = QHBoxLayout()
        buttons_box.setLayout(buttons_layout)

        self.create_worker_button = QPushButton("Добавить контролёра")
        buttons_layout.addWidget(self.create_worker_button)
        self.create_worker_button.clicked.connect(self.create_worker)

        self.to_personal_button = QPushButton("Назад")
        buttons_layout.addWidget(self.to_personal_button)
        self.to_personal_button.clicked.connect(self.to_personal)

        layout.addWidget(buttons_box)

    def create_worker(self):
        login = self.login.text().lower()
        if not login:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите логин")
            return

        password = self.password.text()
        if not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите пароль")
            return

        cursor.execute(f"SELECT * FROM users WHERE login = '{login}'")
        user = cursor.fetchone()

        if user:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Пользователь с таким логином уже существует"
            )
            return

        cursor.execute(
            "INSERT INTO users (login, password, role) VALUES (%s, %s, %s)",
            (login, password, 2),
        )
        db.commit()

        QtWidgets.QMessageBox.information(self, "Успех", "Пользователь создан")



    def to_personal(self):
        self.deleteLater()
        self.parent.to_personal()
