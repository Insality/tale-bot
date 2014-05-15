class test:
	a = 0
	b = 1
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def printinfo(self):
		print self.a, self.b

abc = test(3, 2)
abc.printinfo()