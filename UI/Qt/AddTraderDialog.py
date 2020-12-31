from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import TradeSystem
from Strategies.Strategy import Strategy


class AddTraderDialog(QDialog):

	def __init__(self):
		super(AddTraderDialog, self).__init__()
		uic.loadUi('UI/Qt/source/AddTraderDialog.ui', self)

	def accept(self) -> None:
		TradeSystem.add_trader(Strategy)

		super(AddTraderDialog, self).accept()
