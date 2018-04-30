def unittests(tempCodeString):
	try:
		exec(tempCodeString)
		assert fibonacci(1) == 0
		assert fibonacci(2) == 1
		assert fibonacci(3) == 1
		assert fibonacci(5) == 3
		assert fibonacci(8) == 13
		assert fibonacci(9) == 21
		# print 'Following Case Passed:'
		# print tempCodeString
		return True
	except:
		# print "A test case failed"
		return False