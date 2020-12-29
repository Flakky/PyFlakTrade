import Trader
import typing
import Strategies.Strategy as Strategy
import UI.Qt.MainWindow as MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication

traders: typing.List[Trader.Trader] = []


def add_trader(strategy: Strategy.Strategy.__class__, **kwargs):
    trade_strategy = strategy()

    trader_budget = kwargs.get("budget", 1000)
    trader_max_value = kwargs.get("max_value", 200)
    trader_stocks = kwargs.get("stocks", [])
    trader = Trader.Trader(trade_strategy, trader_budget, trader_max_value, trader_stocks)

    traders.append(trader)


def init():
    app = QApplication(sys.argv)
    main_window = MainWindow.MainWindow()
    main_window.show()
    app.exec_()
