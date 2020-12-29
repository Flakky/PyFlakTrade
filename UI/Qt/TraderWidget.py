from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class TraderWidget(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        uic.loadUi('UI/Qt/source/TraderWidget.ui', self)
