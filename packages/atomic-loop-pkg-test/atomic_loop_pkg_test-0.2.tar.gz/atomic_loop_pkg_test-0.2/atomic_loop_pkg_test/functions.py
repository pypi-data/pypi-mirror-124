
class MathFunctions:
    
	'''Description: This project provides powerful math functions
			|For example, you can use `sum()` to sum numbers:
			|
			|Example1::
			|
			|    >>> sum(1, 2)
			|    3
			|
   			|For example, you can use `sub()` to subtract numbers:
			|
			|Example2::
			|
			|    >>> sub(3, 2)
			|    1
			|'''

	def __init__(self,n1,n2) -> None:
		self.n1 = n1
		self.n2 = n2
	
	def sum(self):
		
		return self.n1+self.n2

	def sub(self):
		return self.n1-self.n2


