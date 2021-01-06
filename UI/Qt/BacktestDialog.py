from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLineEdit, QSpinBox, QDateTimeEdit
import StocksReciever
import StockValue
from datetime import datetime


class BacktestDialog(QDialog):
	stock: str = ""
	budget: int = 1000
	start: datetime = datetime.now()
	end: datetime = datetime.now()
	stock_textedit: QLineEdit
	budget_spinbox: QSpinBox
	start_edit: QDateTimeEdit
	end_edit: QDateTimeEdit

	def __init__(self):
		super(BacktestDialog, self).__init__()
		uic.loadUi('UI/Qt/source/BacktestDialog.ui', self)

		self.stock_textedit = self.lineEdit_Stock
		self.budget_spinbox = self.spinBox_Budget
		self.start_edit = self.dateTimeEdit_Start
		self.end_edit = self.dateTimeEdit_End

		self.start_edit.setDateTime(self.start)
		self.end_edit.setDateTime(self.end)

	def accept(self) -> None:
		self.stock = self.stock_textedit.text()
		self.budget = self.budget_spinbox.value()
		self.start = self.start_edit.dateTime()
		self.end = self.end_edit.dateTime()

		super(BacktestDialog, self).accept()
