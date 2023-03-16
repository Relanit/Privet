from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QScrollArea, QHBoxLayout,
)

from sql import cursor


class ViewLabVesselsWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setCentralWidget(QWidget())

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.centralWidget().setLayout(layout)

        cursor.execute("SELECT * FROM lab_vessels")
        vessels = cursor.fetchall()

        scroll_area = QScrollArea()
        container = QWidget()
        scroll_layout = QHBoxLayout(container)

        columns_box = QGroupBox()
        columns_layout = QGridLayout()
        columns_box.setLayout(columns_layout)

        self.to_admin_button = QPushButton("Назад")
        columns_layout.addWidget(self.to_admin_button, 0, 0)
        self.to_admin_button.clicked.connect(self.to_admin)

        columns_layout.addWidget(QLabel("ID"), 1, 0)
        columns_layout.addWidget(QLabel("Название"), 1, 1)
        scroll_layout.addWidget(columns_box)

        for i, vessel in enumerate(vessels, start=2):
            columns_layout.addWidget(QLabel(str(vessel[0])), i, 0)
            columns_layout.addWidget(QLabel(vessel[1]), i, 1)

        scroll_layout.addWidget(columns_box)
        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

    def to_admin(self):
        self.deleteLater()
        self.parent.to_admin()
