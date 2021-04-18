from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes

import Trader
import Position
from UI.Qt.BacktestDialog import BacktestDialog
import StocksReciever
import StockValue


class PlotCanvas(FigureCanvas):
	axes: Axes = None

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
			QSizePolicy.Expanding,
			QSizePolicy.Expanding
		)

		FigureCanvas.updateGeometry(self)
		self.plot()

	def plot(self):
		self.axes.plot([1,2,3,4], [1,5,2,6])
		return


class TradingPlotWidget(QWidget):
	trader: Trader.Trader = None
	vbox_plotwidget: QVBoxLayout = None
	plotwidget: PlotCanvas

	def __init__(self, trader: Trader.Trader):
		super(TradingPlotWidget, self).__init__()
		uic.loadUi('UI/Qt/source/TradingPlotWidget.ui', self)

		self.trader = trader

		self.vbox_plotwidget = self.verticalLayout_Plot

		self.plotwidget = PlotCanvas(self)

		self.vbox_plotwidget.addWidget(self.plotwidget, 1)
