def loadScript(fname,lines):
    with open(fname) as f:
        for i, l in enumerate(f):
			lines.append(l)
    return i + 1



block_size = 5
buggedLineNo = 7




lines = []
loadScript('mid.py', lines)


lines = [1,2,3,4,5,6,7,8,9,10,11,12,13]

# print lines[buggedLineNo-1]

for i in range(0,len(lines)):
	if (i+2 < len(lines)):
		if i >= buggedLineNo-block_size and i <= buggedLineNo-4+block_size:
		# if i >= buggedLineNo-3 and i <= buggedLineNo-1:
			# print buggedLineNo-3, buggedLineNo-1
		# if i == buggedLineNo-1 or i+1 == buggedLineNo-1 or i+2 == buggedLineNo-1 or i+3 == buggedLineNo-1 or i+4 == buggedLineNo-1:
			print 'skipped'
			# print lines[i], lines[i+1], lines[i+2]
		else:
			print lines[i], lines[i+1], lines[i+2]
	# print 'next'