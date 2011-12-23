from .lookuptree import LookupTree 

class ImmutableVector:
	def __init__(self, initvalues=None):
		if not initvalues: initvalues = []
		self.tree = LookupTree(initvalues)
		self._length = len(initvalues)

	def assoc(self, index, value):
		newvec = ImmutableVector()
		newvec.tree = self.tree.assoc(index, value)
		if index >= self._length:
			newvec._length = index+1
		else:
			newvec._length = self._length
		return newvec

	def concat(self, tailvec):
		newvec = ImmutableVector()
		vallist = [(i + self._length, tailvec[i]) \
				for i in range(0, tailvec._length)]
		newvec.tree = self.tree.multi_assoc(vallist)
		newvec._length = self._length + tailvec._length
		return newvec

	def pop(self):
		if self._length == 0:
			raise IndexError()
		newvec = ImmutableVector()
		newvec.tree = self.tree.remove(self._length-1)
		newvec._length = self._length-1
		return newvec

	def conj(self, value):
		return self.assoc(self._length, value)

	def __iter__(self):
		for i in range(0, self._length):
			yield self[i]

	def __len__(self):
		return self._length

	def __getitem__(self, index):
		if index >= self._length: raise IndexError()
		return self.tree[index]

