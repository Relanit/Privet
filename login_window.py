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


class LoginWindow(QMainWindow):
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

        self.login_button = QPushButton("Авторизация")
        buttons_layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.log_in)

        self.signup_button = QPushButton("Регистрация")
        buttons_layout.addWidget(self.signup_button)
        self.signup_button.clicked.connect(self.sign_up)

        layout.addWidget(buttons_box)

    def log_in(self):
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

        if not user:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Пользователь не найден, зарегистрируйтесь"
            )
            return

        if password != user[2]:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Неверный пароль"
            )
            self.password.setText("")
            return

        QtWidgets.QMessageBox.information(self, "Успех", "Вы авторизовались")

        self.parent.to_admin(login)

    def sign_up(self):
        login = self.login.text().lower()
        if not login:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите логин")
            return

        password = self.password.text()
        if not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите пароль")
            return

        cursor.execute(f"SELECT * FROM users WHERE login = '{login}'")
        if user := cursor.fetchone():
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Пользователь уже зарегестрирован"
            )
            return

        cursor.execute(
            "INSERT INTO users (login, password) VALUES (%s, %s)",
            (login, password),
        )
        db.commit()

        QtWidgets.QMessageBox.information(self, "Успех", "Вы зарегистрированы")
        self.parent.to_admin(login)
