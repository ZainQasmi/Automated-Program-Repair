def unittests(tempCodeString):
	try:
		exec(tempCodeString)
		assert bubbleSort([2,1,3]) == [1,2,3]
		assert bubbleSort([3,3,5]) == [3,3,5]
		assert bubbleSort([1,2,3]) == [1,2,3]
		assert bubbleSort([5,5,5]) == [5,5,5]
		assert bubbleSort([5,3,4]) == [3,4,5]
		assert bubbleSort([3,2,1]) == [1,2,3]
		# print 'Following Case Passed:'
		# print tempCodeString
		return True
	except:
		# print "A test case failed"
		return False