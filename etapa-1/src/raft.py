from pysyncobj import SyncObj, replicated
import sys

class MyCounter(SyncObj):
	# def __init__(self):
	# 	super(MyCounter, self).__init__('serverA:4321', ['serverB:4321', 'serverC:4321'])
	# 	self.__counter = 0

	def __init__(self, selfNodeAddr, otherNodeAddrs):
		super(MyCounter, self).__init__(selfNodeAddr, otherNodeAddrs)
		self.__counter = 0

	@replicated
	def incCounter(self):
		self.__counter += 1
		return self.__counter

	def getCounter(self):
		return self.__counter

def main():
	x,y,z = 1234,1235,1236

	if sys.argv[1] == "x":
		c = MyCounter('localhost:%d' % x,['localhost:%d' % y, 'localhost:%d' % z])
	elif sys.argv[1] == "y":
		c = MyCounter('localhost:%d' % y,['localhost:%d' % x, 'localhost:%d' % z])
	elif sys.argv[1] == "z":
		c = MyCounter('localhost:%d' % z,['localhost:%d' % x, 'localhost:%d' % y])

	while True:
		n = int(input("Type in operation: "))

		if n == 1:
			c.incCounter()
			print(f"Update!")
		elif n == 2:
			s = c.getCounter()
			print(f"Read: {s}")
		else:
			print("End")
			return


if __name__ == "__main__":
	main()