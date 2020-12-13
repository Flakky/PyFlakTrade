import Position
import StockValue


class Strategy:

	def shouldOpenPosition(self, trade_data: list[StockValue.StockValue]):
		return True

	def shouldClosePosition(self, trade_data: list[StockValue.StockValue], position: Position.Position):
		if position is not None:
			last_value = trade_data[-1]
			if last_value.close_value < position.stop_loss or last_value.close_value > position.take_profit:
				return True
			else:
				return False
		else:
			return False
