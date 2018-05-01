def mid(x,y,z):
	m = z
	a = x
	b = y
	c = z
	n = m
	if (y<z):
		if(x<y):
			m = y
		elif (x<z):
			m = y
	else:	
		if(a>b):
			n = b
		elif (a>c):
			n = a
		m = n
	return m