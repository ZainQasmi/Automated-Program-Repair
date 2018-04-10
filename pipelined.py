#################################################################
# Project Title		: Automated Program Repair		 			#
# Instructor 		: Junaid Haroon Siddiqui					#
# Duration 			: Fall 2017 - Spring 2018					#
# University		: Lahore University of Management Sciences	#
# Authors 			: Ali Ahsan 								#
# 					: Dawood Jehangir							# 
# 					: Muhammad Zain Qasmi						#
# Roll No. 			: 18100XXX && 18100XXX && 18100XXX			#
# Submission 		: May, 2018									#
# Python Version 	: 2.7										#
#################################################################

# We assume user makes one error at a time i.e. he either uses 
# incorrect operator or incorrect variable.

#==============================================================================#

import sys
import ast
import re
import random
import string
from itertools import permutations
from itertools import combinations

### Writes test filename and test result filename to file which will be used by tarantula.py
with open("importNames.csv", "w") as text_file:
    text_file.write("%s,%s" %(sys.argv[1],sys.argv[2])) 

### Executes tarantula which isolates the bugged line and stores it in list lines. 
### The line with highest likelihood of having a bug is at first index i.e. lines[0]
print '//===----------------------- Running Tarantula ------------------------===//'
execfile('tarantula.py')
print '//===----------------------- Returns Tarantula ------------------------===//'

print
buggedLine = lines[0].lineNo
print '//===-----------------------    Bugged Line    ------------------------===//'
print lines[0].text.strip()


def loadScript(fname,lines):
    with open(fname) as f:
        for i, l in enumerate(f):
			lines.append(l)
    return i + 1

def makeVarListFile(sourceScript):
	with open(sourceScript, 'r') as myfile:
	    source=myfile.read()
	root = ast.parse(source)
	vars = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
	return vars

def makeVarList(sourceLine):
	root = ast.parse(sourceLine)
	vars = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
	return vars

def makeVarCombination(totalVariables, lenBuggedVars):
	tempVarList = []
	for c in combinations(totalVariables, lenBuggedVars):
		for p in permutations(c):
			tempVarList.append(p)
	return tempVarList

# program restricted to 26 vars. Fcuk my life
def returnSuggestedLine(line_to_fix, buggedVarList, suggestedVarListofLists, codeToEdit, original_code):
	# print 'line actual: ',line_to_fix
	# print buggedVarList
	tempLine = line_to_fix
	tempCodeString = ''
	counter = 0;
	print

	breakAtIter = 2
	for oneList in suggestedVarListofLists:
		# if breakAtIter == 0:
		# 	break
		# breakAtIter -=1
		tempLine = line_to_fix
		# print tempLine
		# print oneList
		for i in range(0,len(buggedVarList)):
			temp = '([^\w\D]*\\b' + buggedVarList[i] + '\\b)|([^\w\D]*' + buggedVarList[i] + '[_\d]+)'
			tempLine = re.sub(temp, oneList[i], tempLine)
			# print buggedVarList[i], ' ', oneList[i], ' ', tempLine
			counter +=1
		# print 'new :: ',tempLine

		# print len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())
		tabsToAdd = len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())
		for i in range (0,tabsToAdd):
			tempLine = '\t' + tempLine
		codeToEdit[buggedLine-1] = tempLine
		# print len(tempLine) - len(tempLine.lstrip())

		for line in codeToEdit:
			tempCodeString += line + '\n'
			# print line

		testRepairedCode(tempCodeString, original_code)
	# print counter

def testRepairedCode(tempCodeString, original_code):
	pass
	# test_mid.test_mid(tempCodeString)
	# potentiallyCorrect = True
	# for oneCase in testCaseResuts:

	# 	strInput = oneCase[0]
	# 	tupleofIntCastedInput = tuple(map(int, strInput.split(',')))
		
	# 	exec(original_code)
	# 	originalCodeOutput = mid(*tupleofIntCastedInput)
	# 	# print 'ori', originalCodeOutput

	# 	exec(tempCodeString)
	# 	suggestedCodeOutput = mid(*tupleofIntCastedInput)
	# 	print 'sug', originalCodeOutput, tempCodeString

	# 	if oneCase[1] == 'P':
	# 		if originalCodeOutput == suggestedCodeOutput:
	# 			pass
	# 			# print 'so far so good'
	# 		else:
	# 			# print 'FUBAR. Next'
	# 			potentiallyCorrect = False
	# 	elif oneCase[1] == 'F':
	# 		if originalCodeOutput == suggestedCodeOutput:
	# 			# print 'this should be different'
	# 			potentiallyCorrect = False
	# 		else:
	# 			pass
	# 			# print 'hmm...see if this is right'

	# 	if potentiallyCorrect == True:
	# 		print oneCase
			# print suggestedCodeOutput, originalCodeOutput
		# print 'sug', suggestedCodeOutput


	# print "Function returns ::",suggestedCodeOutput

def main():
	testFileName = sys.argv[1]
	resultsFileName = sys.argv[2]

	execfile('testMid.py')

	# testingCodeFileName = sys.argv[3]
	# print testingCodeFileName

	# with open(testingCodeFileName) as source_file:
    	# exec(source_file.read())

	lines = []
	loadScript(testFileName, lines)

	codeToEdit = []
	for line in lines:
		codeToEdit.append(line.rstrip())
		# print line.rstrip()
	original_code = '\n'.join(codeToEdit)

	line_to_fix = lines[buggedLine-1].rstrip()
	# print line_to_fix.strip()

	totalVariables = makeVarListFile(testFileName)
	# print totalVariables

	tempLine = line_to_fix.strip()
	if line_to_fix[len(line_to_fix)-1] == ':':
		tempLine = line_to_fix.strip() + 'pass'

	buggedVariables = makeVarList(tempLine)
	# print buggedVariables

	suggestedVarListofLists = makeVarCombination(totalVariables, len(buggedVariables))
	returnSuggestedLine(line_to_fix.strip(),buggedVariables,suggestedVarListofLists, codeToEdit, original_code)
	
if __name__ == "__main__":
    main()
