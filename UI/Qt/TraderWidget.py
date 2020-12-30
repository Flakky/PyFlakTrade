from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import Trader


class TraderWidget(QWidget):
    trader: Trader.Trader = None

    def __init__(self, trader: Trader.Trader):
        super(TraderWidget, self).__init__()
        uic.loadUi('UI/Qt/source/TraderWidget.ui', self)

        self.trader = trader
