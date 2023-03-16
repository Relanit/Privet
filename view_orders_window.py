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


class ViewOrdersWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setCentralWidget(QWidget())

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.centralWidget().setLayout(layout)

        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        scroll_area = QScrollArea()
        container = QWidget()
        scroll_layout = QVBoxLayout(container)

        self.to_admin_button = QPushButton("Назад")
        scroll_layout.addWidget(self.to_admin_button)
        self.to_admin_button.clicked.connect(self.to_admin)

        for order in orders:
            order_box = QGroupBox()
            order_layout = QVBoxLayout()
            order_box.setLayout(order_layout)

            order_layout.addWidget(QLabel(f"id: {order[0]}"))
            order_layout.addWidget(QLabel(f"Клиент: {order[1]}"))
            order_layout.addWidget(QLabel(f"Код лабораторного сосуда: {order[2]}"))
            services = QLabel(f"Услуги: {order[3]}")
            services.setWordWrap(True)
            order_layout.addWidget(services)
            order_layout.addWidget(QLabel(f"Общая сумма заказа: {order[4]}"))
            scroll_layout.addWidget(order_box)

        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

    def to_admin(self):
        self.deleteLater()
        self.parent.to_admin()
