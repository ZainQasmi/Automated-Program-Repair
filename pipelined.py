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
import tokenize, token
from itertools import permutations
from itertools import combinations

### Writes test filename and test result filename to file which will be used by tarantula.py
with open("importNames.csv", "w") as text_file:
    text_file.write("%s,%s" %(sys.argv[1],sys.argv[2])) 

### Executes tarantula which isolates the bugged line and stores it in list lines. 
### The line with highest likelihood of having a bug is at first index i.e. lines[0]
print '//===----------------------- Running Tarantula ------------------------===//'
execfile('tarantula.py')
# print '//===----------------------- Returns Tarantula ------------------------===//'

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
def tryOperatorsReplacement(line_to_fix, buggedVarList, suggestedVarListofLists, codeToEdit, original_code):
	pass

def tryVaribleReplacement(line_to_fix, buggedVarList, suggestedVarListofLists, codeToEdit, original_code):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically
	
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
			tempLine = re.sub(temp, oneList[i], tempLine) #substitute
			# print buggedVarList[i], ' ', oneList[i], ' ', tempLine
			counter +=1
		# print 'new :: ',tempLine

		# print len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())

		# Calculate and add requisite no. of tabs to the changed line of code
		tabsToAdd = len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())
		for i in range (0,tabsToAdd):
			tempLine = '\t' + tempLine
		codeToEdit[buggedLine-1] = tempLine
		# print len(tempLine) - len(tempLine.lstrip())

		for line in codeToEdit:
			tempCodeString += line + '\n'
			# print line
		# print tempLine

		if testRepairedCode.unittests(tempCodeString):
			print '//===------------------------ Code with Bug Fix -----------------------===//'
			print tempCodeString

	# print counter

def get_buggyLine_operators(line):
	operators = []
	for t in tokenize.generate_tokens(iter([line]).next):
	    if token.tok_name[t[0]] == 'OP':
	    	operators.append(t[1])

	return operators

def get_list_of_all_operator_combiantions(line,operators):
	o1 = ['+','-','*','/','%','**'] #arithematic ** //
	o2 = ['==','!=','<','>','>=','<='] #comparison 
	o3 = ['=','+=','-=','*='] #assignment ,'**=','//='
	o4 = o1+o2+o3
	tempOpList = []
	numberOp = len(operators)
	for c in combinations(o4, numberOp):
			for p in permutations(c):
				tempOpList.append(p)

	## all possible combinations of operators generated
	return tempOpList

def generate_new_lines_with_all_operator_combinations(line,operators,operator_combinations):
	abc_list = list(string.ascii_uppercase)
	new_lines = []
	for it in range(0,len(operator_combinations)):
		temp_combination = list(operator_combinations[it])

		temp_line = line
		
		replace_list=[]
		abc_index=0
		for i in range(0,len(temp_combination)):
			if temp_combination[i] in operators[i+1:]:
				replace_list.append([temp_combination[i],abc_list[abc_index]])
				temp_line = temp_line.replace(operators[i],abc_list[abc_index])
				abc_index+=1
			else:
				temp_line = temp_line.replace(operators[i],temp_combination[i])

		for i in range(0,len(replace_list)):
			temp_line = temp_line.replace(replace_list[i][1],replace_list[i][0])

		new_lines.append(temp_line)

	return new_lines

def main():
	testFileName = sys.argv[1]
	resultsFileName = sys.argv[2]

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
	tryVaribleReplacement(line_to_fix.strip(),buggedVariables,suggestedVarListofLists, codeToEdit, original_code)

	# line_to_fix = 'a=b**c-2'
	ops = get_buggyLine_operators(line_to_fix)
	op_combinations = get_list_of_all_operator_combiantions(line_to_fix,ops)
	corrected_lines = generate_new_lines_with_all_operator_combinations(line_to_fix,ops,op_combinations)

	# print ops
	# for op in op_combinations:
		# print op[0]
	# for oneLiner in corrected_lines:
	# 	print oneLiner
	# print line_to_fix.strip()


if __name__ == "__main__":
    main()
