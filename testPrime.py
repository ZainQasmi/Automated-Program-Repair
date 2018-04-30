def unittests(tempCodeString):
	try:
		exec(tempCodeString)
		assert is_prime(3) == True
		assert is_prime(4) == False
		assert is_prime(5) == True
		assert is_prime(6) == False
		assert is_prime(7) == True
		assert is_prime(9) == False
		assert is_prime(11) == True
		assert is_prime(-2) == False
		# print is_prime(3)
		# print is_prime(4)
		# print is_prime(5)
		# print is_prime(6)
		# print is_prime(7)
		# print is_prime(9)
		# print is_prime(11)
		# print is_prime(-2)
		# print 'Following Case Passed:'
		# print tempCodeString
		return True
	except:
		# print "A test case failed"
		return False
