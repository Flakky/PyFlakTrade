from Position import Position
from Observer import Observer


class TradeProvider:
	budget: float = 0.0
	on_position_opened: Observer = Observer()
	on_position_closed: Observer = Observer()
	
	def open_position(self, position: Position):
		
		print("""Position open: 
		{pos}
		Budget: {budget}""".format(pos=str(position), budget=self.budget))
		
		self.on_position_opened.exec(position)
		
		return
		
	def close_position(self, position: Position):
		print("""Position close: 
		{pos}
		
		Budget: {budget}""".format(pos=str(position), budget=self.budget))

		self.on_position_closed.exec(position)
		
		return
		
	def read_budget(self) -> float:
		return self.budget
