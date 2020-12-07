import StocksReciever
import Position

class Trader:
    openedPosition = None
    closedPositions = []
    tradeInProgress = False
    backtest = {
    	"testMode": False,
    	"tradeData": {},
    	"testCurrentTime": None
    }
    
    def __init__(self, strategy, budget, position_max_value):
    	self.strategy = strategy
    	self.budget = budget
    	self.posMaxValue = position_max_value


	def update(self)
		if(strategy is None):
			return
		
		tradeData = self.recieveTradeData()
		
		if(openedPosition is not None):
			if(strategy.shouldClosePosition(tradeData, openedPosition)):
				closePosition()
		else:
			if(strategy.shouldOpenPosition(tradeData)):
				openValue = tradeData[-1].value
				position = Position(
					0, 
					openValue,
					1,
					stopLoss=openValue-(openValue/100),
					takeProfit=openValue+(openValue/100*2)
				 )
				openPosition(position)


    def openPosition(self, position):
        self.openedPosition = position
        
        self.budget -= position.open_value
        
        print("Position open: {p}".format(p=str(position)))


    def closePosition(self, time, value):
        self.openedPosition.close(time, value)
        self.closedPositions.append(self.openedPosition)
        
        self.budget += value;
        
        print("Position close: {p}".format(p=str(position)))
        
        self.openedPosition = None
        
        
	def recieveTradeData(self):
		tradeData = {"12.01.2020, 23.54": 125.534}


	def start(self):
		self.tradeInProgress = True
		while self.tradeInProgress:
			self.update()
			sleep(5)
			
	
	def stop(self):
		self.tradeInProgress = False
		
		
	def enableBacktestMode(self, test_trade_data):
		self.backtest["testMode"] = True
		self.backtest["tradeData"] = test_trade_data