from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QPushButton
from UI.Qt.AddTraderDialog import AddTraderDialog
from UI.Qt.TraderWidget import TraderWidget
import TradeSystem


class MainWindow(QMainWindow):
    add_trader_dialog: AddTraderDialog = None
    traders_tab_widget: QTabWidget = None

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('UI/Qt/source/MainWindow.ui', self)

        action = self.findChild(QAction, "actionAdd_trader")
        self.actionAdd_trader.triggered.connect(self.show_add_trader_dialog)

        traders_tab_widget = self.findChild(QTabWidget, "traders_tab_widget")

    def show_add_trader_dialog(self):
        self.add_trader_dialog = AddTraderDialog()
        self.add_trader_dialog.show()

        self.add_trader_dialog.accepted.connect(self.accept_add_trader)
        self.add_trader_dialog.rejected.connect(self.reject_add_trader)

    def accept_add_trader(self):
        self.add_trader_dialog = None

        trader_widget = TraderWidget(TradeSystem.traders[-1])
        self.traders_tab_widget.addTab(trader_widget, "Trader"+str(len(TradeSystem.traders)))

    def reject_add_trader(self):
        self.add_trader_dialog = None
