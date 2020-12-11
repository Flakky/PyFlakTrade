import Position


class Strategy:

	def shouldOpenPosition(self, trade_data):
		return True

	def shouldClosePosition(self, trade_data, position):
		if position is not None:
			last_value = trade_data[-1]
			if last_value > position.stop_loss or last_value < position.take_profit:
				return True
			else:
				return False
		else:
			return False
