class Observer:

	def __init__(self):
		self.callbacks = []

	def subscribe(self, callback):
		self.callbacks.append(callback)

	def exec(self, *args, **kwargs):
		for callback in self.callbacks:
			callback(*args, **kwargs)
