from Trader import Trader
import typing

traders: typing.List[Trader] = []

def add_trader(trader: Trader):
	traders.append(trader)

	print("Trader added")


def init():
	print("Trade system init")
