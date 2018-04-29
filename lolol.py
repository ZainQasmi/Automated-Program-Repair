def mid(y,z,x):
	m = z
	if (y<z):
		if(x<y):
			print 'lul'
			m = a
		elif (x<z):
			print 'lul'
			m = a
	else:
		if(x>y):
			m = y
		elif (x>z):
			m = x
	return m

def unittests():
	try:
		# exec(tempCodeString)
		assert mid(2,1,3) == 2
		assert mid(3,3,5) == 3
		assert mid(1,2,3) == 2
		assert mid(5,5,5) == 5
		assert mid(5,3,4) == 4
		assert mid(3,2,1) == 2
		# print 'Following Case Passed:'
		# print tempCodeString
		return True
	except:
		# print "A test case failed"
		return False

print unittests()