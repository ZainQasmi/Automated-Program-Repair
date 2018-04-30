class listTupleLogic:

	def __init__(self):
		self.lists = {}
		self.tuples = {}
		self.startList = []
		self.startTuple = []

	def pushList(self, index):
		self.startList.append(index)


	def popList(self, index):
		i = self.startList[len(self.startList)-1]
		self.lists[i] = index
		del self.startList[-1]


	def pushTuple(self, index):
		self.startTuple.append(index)


	def popTuple(self, index):
		i = self.startTuple[len(self.startTuple)-1]
		self.tuples[i] = index
		del self.startTuple[-1]
