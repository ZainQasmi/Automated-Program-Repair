# from __future__ import print_function

def pascal(n):
	a=[]
	for i in range(n):
	    a.append([])
	    a[i].append(1)
	    for j in range(1,i):
	        a[i].append(a[i-1][j-1]+a[i-1][j])
	    if(n!=0):
	        a[i].append(1)
	for i in range(n):
	    print ("   "*(n-i))
	    for j in range(0,i+1):
	        print '{0:6}'.format(a[i][j]),end=" ",sep=" "
	    print()

def unittests(tempCodeString):
	try:
		# exec(tempCodeString)
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

print (unittests('lol'))

print ( pascal(1) )
print ( pascal(2) )
print ( pascal(3) )
print ( pascal(5) )
print ( pascal(8) )
print ( pascal(9) )
