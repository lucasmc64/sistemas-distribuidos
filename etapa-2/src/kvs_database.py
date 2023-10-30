from pysyncobj import SyncObj, replicated
import sys

class KVSDataBase(SyncObj):

	def __init__(self, selfDBAddress, otherDBAddresses):
		super(KVSDataBase, self).__init__(selfDBAddress, otherDBAddresses)
		self.__counter = 0

	@replicated
	def incCounter(self):
		self.__counter += 1
		return self.__counter

	def getCounter(self):
		return self.__counter

def main():
	bd1,bd2,bd3 = 1234,1235,1236

	if sys.argv[1] == "bd1":
		c = KVSDataBase('localhost:%d' % bd1,['localhost:%d' % bd2, 'localhost:%d' % bd3])
	elif sys.argv[1] == "bd2":
		c = KVSDataBase('localhost:%d' % bd2,['localhost:%d' % bd1, 'localhost:%d' % bd3])
	elif sys.argv[1] == "bd3":
		c = KVSDataBase('localhost:%d' % bd3,['localhost:%d' % bd1, 'localhost:%d' % bd2])

	while True:
		print("Operations")
		print("1 - Increase counter")
		print("2 - Get counter value")
		print("3 - Exit")
		n = input("Type in operation (1, 2 or 3): ")
		if n == "":
			continue
		n = int(n)

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