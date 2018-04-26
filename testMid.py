def unittests(tempCodeString):
	exec(tempCodeString)
	try:
		assert mid(2,1,3) == 2
		assert mid(3,3,5) == 3
		assert mid(1,2,3) == 2
		assert mid(5,5,5) == 5
		assert mid(5,3,4) == 4
		assert mid(3,2,1) == 2
		# print 'Following Case Passed:'
		# print tempCodeString
		return True
	except AssertionError:
		# print "A test case failed"
		return False