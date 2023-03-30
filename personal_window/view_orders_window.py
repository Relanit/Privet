import traceback

from PyQt6 import QtWidgets
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

from sql import cursor, db


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
        self.widgets = []
        self.to_personal_button = QPushButton("Назад")
        scroll_layout.addWidget(self.to_personal_button)
        self.to_personal_button.clicked.connect(self.to_personal)

        role = self.parent.personal_window.role

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

            if role == 2 and not order[5]:
                self.check_order_button = QPushButton("Одобрить")
                order_layout.addWidget(self.check_order_button)
                self.check_order_button.clicked.connect(lambda _, index=order[0]: self.check_order(index))

            else:
                order_layout.addWidget(QLabel(f"Статус: {'одобрено' if order[5] else 'не проверено'}"))

            if role == 2:
                self.delete_order_button = QPushButton("Удалить")
                order_layout.addWidget(self.delete_order_button)
                self.delete_order_button.clicked.connect(lambda _, index=order[0]: self.delete_order(index))

            scroll_layout.addWidget(order_box)

        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)


    def to_personal(self):
        self.deleteLater()
        self.parent.to_personal()

    def check_order(self, index):
        cursor.execute(
            f"UPDATE orders SET checked = 1 WHERE id = {index}",
        )
        db.commit()

        QtWidgets.QMessageBox.information(self, "Успех", "Заказ одобрен")
        self.init_ui()

    def delete_order(self, index):
        cursor.execute(
            f"DELETE FROM orders WHERE id = {index}",
        )
        db.commit()

        QtWidgets.QMessageBox.information(self, "Успех", "Заказ удалён")
        self.init_ui()
