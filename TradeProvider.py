from Position import Position

class TradeProvider:
	budget: float = 0.0
	
	def open_position(self, position: Position):
		
		print("""Position open: 
		{pos}
		Budget: {budget}""".format(pos=str(position), budget=self.budget))
		
		return
		
	def close_position(self, position: Position):
		print("""Position open: 
		{pos}
		
		Budget: {budget}""".format(pos=str(position), budget=self.budget))

		return
		
	def read_budget(self) -> float:
		return self.budget
		