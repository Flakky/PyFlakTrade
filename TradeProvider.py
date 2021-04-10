class TradeProvider:
	budget: float = 0.0
	
	def open_position(self, ticker: str, amount: int):
		return
		
	def close_position(self, ticker: str, amount: int):
		return
		
	def read_budget(self) -> float:
		return self.budget
		