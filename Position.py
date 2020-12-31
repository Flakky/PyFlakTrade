import datetime
import typing


class Position:
	open_time: datetime.datetime = datetime.datetime.min
	close_time: datetime.datetime = datetime.datetime.min
	open_value: float = 0.0
	close_value: float = 0.0
	amount: int = 1
	stop_loss: float = 0.0
	take_profit: float = 99999999.0
	closed: bool = False

	def __init__(self, time: datetime.datetime, value: int, amount: int = 1, **kwargs):
		self.open_time = time
		self.open_value = value
		self.amount = amount
		self.stop_loss = kwargs.get("stop_loss", 0)
		self.take_profit = kwargs.get("take_profit", 99999)

	def close(self, time: datetime.datetime, value: float):
		self.close_time = time
		self.close_value = value
		self.closed = True

	def __str__(self):
		return """Position:
    -Open: {open} - {open_time}
    -{close}
    -Amount: {amount}
    -Stop: {stop}
    -Take: {take}""".format(
			close="Close: {color} {close} \033[0m - {close_time}".format(
				close=round(self.close_value, 3),
				close_time=self.close_time,
				color="\033[92m" if self.close_value > self.open_value
				else ("" if self.close_value == self.open_value else "\033[91m")
			) if self.closed else "Not closed",
			open=round(self.open_value, 3),
			amount=self.amount,
			open_time=self.open_time,
			stop=self.stop_loss,
			take=self.take_profit
		)


def get_positions_from_list(positions_list: typing.List[Position], start: datetime.datetime, end: datetime.datetime) -> \
		typing.List[Position]:
	out_list = []
	for position in positions_list:
		if position.open_time >= start and position.close_time <= end:
			out_list.append(position)

	return out_list
