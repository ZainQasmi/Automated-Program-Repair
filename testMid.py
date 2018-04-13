# import mid
def mid(x,y,z):
	m = z
	if (y<z):
		if(x<y):
			m = y
		elif (x<z):
			m = x
	else:
		if(x>y):
			m = y
		elif (x>z):
			m = x
	return m
def test_mid(tempCodeString):
	# exec(tempCodeString)
	try:
		assert mid(2,1,3) == 2
		assert mid(3,3,5) == 3
		assert mid(1,2,3) == 2
		assert mid(5,5,5) == 5
		assert mid(5,3,4) == 4
		assert mid(3,2,1) == 2
		return True
	except AssertionError:
		print "A test case failed"
		return False

test_mid('lol')

# import unittest

# execfile('mid.py')


# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual(mid(3,3,5), 3)
#         self.assertEqual(mid(1,2,3), 2)
#         self.assertEqual(mid(5,5,5), 5)
#         self.assertEqual(mid(5,3,4), 4)
#         self.assertEqual(mid(3,2,1), 2)
#         self.assertEqual(mid(2,1,3), 2)

# if __name__ == '__main__':
#     unittest.main()