class Item(object):
	"Basically the class i'm using to create instantiations of my items"
	def __init__(self, name, c, weight, buy, sell):
		self.name = name
		self.weight = weight
		self.buy = buy
		self.sell = sell
		self.c = c
		self.eff = (sell - buy) / max(0.0001 ,weight)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.__str__()