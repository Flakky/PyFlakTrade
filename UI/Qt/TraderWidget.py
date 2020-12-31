from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
import Trader
import Position
import StocksReciever
import asyncio


class TraderWidget(QWidget):
	trader: Trader.Trader = None
	position_table: QTableWidget = None
	backtest_button: QPushButton = None
	budget: QLabel = None

	def __init__(self, trader: Trader.Trader):
		super(TraderWidget, self).__init__()
		uic.loadUi('UI/Qt/source/TraderWidget.ui', self)

		self.trader = trader
		self.position_table = self.tableWidget
		self.budget = self.label_budget

		print(self.position_table)

		trader.on_position_opened.subscribe(self.add_position)
		trader.on_position_closed.subscribe(self.update_closed_position)

		self.button_backtest.clicked.connect(self.start_backtest)

	def add_position(self, trader: Trader.Trader, position: Position.Position):
		row_index = self.position_table.rowCount()

		self.position_table.insertRow(row_index)

		self.position_table.setItem(row_index, 0, QTableWidgetItem(position.open_time.strftime("%Y-%m-%d %H:%M:%S")))
		self.position_table.setItem(row_index, 1, QTableWidgetItem(str(position.open_value)))
		self.position_table.setItem(row_index, 2, QTableWidgetItem(str(position.amount)))
		self.position_table.setItem(row_index, 3, QTableWidgetItem(str(position.amount * position.open_value)))

		self.budget.setText(str(trader.budget))

	def update_closed_position(self, trader: Trader.Trader, position: Position.Position):
		row_index = self.position_table.rowCount() - 1

		self.position_table.setItem(row_index, 4, QTableWidgetItem(str(position.close_value)))
		self.position_table.setItem(row_index, 5, QTableWidgetItem(str(position.close_value - position.open_value)))
		self.position_table.setItem(row_index, 6, QTableWidgetItem(str((position.close_value - position.open_value)*position.amount)))
		self.position_table.setItem(row_index, 7, QTableWidgetItem(position.close_time.strftime("%Y-%m-%d %H:%M:%S")))

		self.budget.setText(str(trader.budget))

	def start_backtest(self):
		data = StocksReciever.receiveStocks("AMD")

		self.trader.enableBacktestMode(data)

		self.trader.start_async()
