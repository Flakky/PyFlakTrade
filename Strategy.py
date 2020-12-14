import Position
import StockValue
import typing


class Strategy:
	trader = None #TODO: declare a type of Trader
	
	def set_trader(self, trader):
		self.trader = trader

	def shouldOpenPosition(self, trade_data: typing.List[StockValue.StockValue]) -> bool:
		return True

	def shouldClosePosition(self, trade_data: typing.List[StockValue.StockValue], position: Position.Position) -> bool:
		if position is not None:
			last_value = trade_data[-1]
			if last_value.close_value < position.stop_loss or last_value.close_value > position.take_profit:
				return True
			else:
				return False
		else:
			return False
