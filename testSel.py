def unittests(tempCodeString):
	try:
		exec(tempCodeString)
		assert selection_sort([64,25,12,22,11,12]) == [11,12,12,22,25,64]
		assert selection_sort([22,11,12]) == [11,12,22]
		assert selection_sort([64,25,12]) == [12,25,64]
		assert selection_sort([12,12]) == [12,12]
		assert selection_sort([11,12]) == [11,12]
		assert selection_sort([11]) == [11]
		assert selection_sort([12,11]) == [11,12]
		# print 'Following Case Passed:'
		# print tempCodeString
		return True
	except:
		# print "A test case failed"
		return False