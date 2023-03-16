from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QVBoxLayout,
    QScrollArea,
)

from sql import cursor


class ViewClientsWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setCentralWidget(QWidget())

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.centralWidget().setLayout(layout)

        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()

        scroll_area = QScrollArea()
        container = QWidget()
        scroll_layout = QVBoxLayout(container)

        self.to_admin_button = QPushButton("Назад")
        scroll_layout.addWidget(self.to_admin_button)
        self.to_admin_button.clicked.connect(self.to_admin)

        for client in clients:
            client_box = QGroupBox()
            client_layout = QVBoxLayout()
            client_box.setLayout(client_layout)

            client_layout.addWidget(QLabel(f"id: {client[0]}"))
            client_layout.addWidget(QLabel(f"Имя: {client[1]}"))
            client_layout.addWidget(QLabel(f"Номер телефона: {client[2]}"))
            email = QLabel(f"Электронная почта: {client[3]}")
            email.setWordWrap(True)
            client_layout.addWidget(email)
            scroll_layout.addWidget(client_box)

        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

    def to_admin(self):
        self.deleteLater()
        self.parent.to_admin()
