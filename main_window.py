import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
)

from admin_window import AdminWindow
from login_window import LoginWindow
from new_order_window import NewOrderWindow
from new_service_window import NewServiceWindow
from view_clients_window import ViewClientsWindow
from view_lab_vessels_window import ViewLabVesselsWindow
from view_orders_window import ViewOrdersWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 350, 300)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.create_ui()

    def create_ui(self):
        self.login_window = LoginWindow(self)
        self.stacked_widget.addWidget(self.login_window)
        self.setWindowTitle("Вход")

    def to_admin(self, login=None):
        if login:
            self.login_window.deleteLater()
            self.personal_window = AdminWindow(self, login)
            self.stacked_widget.addWidget(self.personal_window)

        self.stacked_widget.setCurrentIndex(0)
        self.setWindowTitle("Страница администратора")

    def to_login(self):
        self.personal_window.deleteLater()
        self.login_window = LoginWindow(self)
        self.stacked_widget.addWidget(self.login_window)
        self.setWindowTitle("Вход")

    def to_new_order(self):
        self.new_order_window = NewOrderWindow(self)
        self.stacked_widget.addWidget(self.new_order_window)
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle("Формирование заказа")

    def to_view_orders(self):
        self.view_orders_window = ViewOrdersWindow(self)
        self.stacked_widget.addWidget(self.view_orders_window)
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle("Список заказов")

    def to_view_clients(self):
        self.view_clients_window = ViewClientsWindow(self)
        self.stacked_widget.addWidget(self.view_clients_window)
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle("Список клиентов")

    def to_view_vessels(self):
        self.view_vessels_window = ViewLabVesselsWindow(self)
        self.stacked_widget.addWidget(self.view_vessels_window)
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle("Список лабораторных сосудов")

    def to_new_service(self):
        self.new_service_window = NewServiceWindow(self)
        self.stacked_widget.addWidget(self.new_service_window)
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle("Создание услуги")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
