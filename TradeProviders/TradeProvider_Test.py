from TradeProviders.TradeProvider import TradeProvider
from Position import Position


class TradeProviderTest(TradeProvider):

	def __init__(self, budget: float):
		self.budget = budget
	
	def open_position(self, position: Position):
		self.budget -= position.amount * position.open_value
		
		super(TradeProviderTest, self).open_position(position)
		
	def close_position(self, position: Position):
		self.budget += position.amount * position.close_value
		
		super(TradeProviderTest, self).close_position(position)
