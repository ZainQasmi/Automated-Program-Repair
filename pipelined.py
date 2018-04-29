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

def tryVariableReplacement(line_to_fix, buggedVarList, suggestedVarListofLists, codeToEdit, original_code):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically

	temp_line = line_to_fix
	tempCodeString = ''
	abc_list = list(string.ascii_uppercase)

	for it in range(0,len(suggestedVarListofLists)):
		temp_combination = list(suggestedVarListofLists[it])
		temp_line = line_to_fix
		replace_list=[]
		abc_index=0
		
		for i in range(0,len(temp_combination)):
			if temp_combination[i] in buggedVarList[i+1:]:
				replace_list.append([temp_combination[i],abc_list[abc_index]])
				temp_line = temp_line.replace(buggedVarList[i],abc_list[abc_index])
				abc_index+=1
			else:
				temp_line = temp_line.replace(buggedVarList[i],temp_combination[i])

		for i in range(0,len(replace_list)):
			temp_line = temp_line.replace(replace_list[i][1],replace_list[i][0])

		## Calculate and add requisite no. of tabs to the changed line of code
		tabsToAdd =  len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())

		for i in range (0,tabsToAdd):
			temp_line = '\t' + temp_line
		codeToEdit[buggedLine-1] = temp_line

		for line in codeToEdit:
			tempCodeString += line + '\n'

		if testRepairedCode.unittests(tempCodeString):
			print '//===------------------------ VAR: Start Code with Bug Fix -----------------------===//'
			print tempCodeString
			print '//===------------------------- VAR: End Code with Bug Fix -----------------------===//'

		tempCodeString = ''
def get_buggyLine_operators(line):
	operators = []
	for t in tokenize.generate_tokens(iter([line]).next):
	    if token.tok_name[t[0]] == 'OP':
	    	operators.append(t[1])
	return operators

def get_list_of_all_operator_combinations(line,operators):
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

def tryOperatorReplacement(line_to_fix, buggedOperators, suggestedOperatorListofLists, codeToEdit, original_code):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically

	temp_line = line_to_fix
	tempCodeString = ''
	abc_list = list(string.ascii_uppercase)

	for it in range(0,len(suggestedOperatorListofLists)):
		temp_combination = list(suggestedOperatorListofLists[it])

		temp_line = line_to_fix
		
		replace_list=[]
		abc_index=0
		for i in range(0,len(temp_combination)):
			if temp_combination[i] in buggedOperators[i+1:]:
				replace_list.append([temp_combination[i],abc_list[abc_index]])
				temp_line = temp_line.replace(buggedOperators[i],abc_list[abc_index])
				abc_index+=1
			else:
				temp_line = temp_line.replace(buggedOperators[i],temp_combination[i])

		for i in range(0,len(replace_list)):
			temp_line = temp_line.replace(replace_list[i][1],replace_list[i][0])

		## Calculate and add requisite no. of tabs to the changed line of code
		tabsToAdd =  len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())

		for i in range (0,tabsToAdd):
			temp_line = '\t' + temp_line
		codeToEdit[buggedLine-1] = temp_line

		for line in codeToEdit:
			tempCodeString += line + '\n'

		if testRepairedCode.unittests(tempCodeString):
			print '//===------------------------ OPR: Start Code with Bug Fix -----------------------===//'
			print tempCodeString
			print '//===------------------------- OPR: End Code with Bug Fix -----------------------===//'

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

	temp_line = line_to_fix.strip()
	if line_to_fix[len(line_to_fix)-1] == ':':
		temp_line = line_to_fix.strip() + 'pass'

	buggedVariables = makeVarList(temp_line)
	suggestedVarListofLists = makeVarCombination(totalVariables, len(buggedVariables))

	############################################################
	# before passing codeToEdit in each function. make codeToEdit=Original_bugged_code. Here original_bugged_code is mid.py in 
	#its original incorrect. Otherwise there are problelms

	# update codeToEdit after every function call. Therefore I have introduced the back_up_code variable, which
	# contains the original incorrect state of mid.py
	back_up_code = codeToEdit
	tryVariableReplacement(line_to_fix.strip(),buggedVariables,suggestedVarListofLists, codeToEdit, original_code)


	codeToEdit = back_up_code

	buggedOperators = get_buggyLine_operators(line_to_fix.strip())
	# print buggedOperators
	suggestedOperatorListofLists = get_list_of_all_operator_combinations(line_to_fix.strip, buggedOperators)
	# print suggestedOperatorListofLists
	tryOperatorReplacement(line_to_fix.strip(), buggedOperators, suggestedOperatorListofLists, codeToEdit, original_code )
	# code = back_up_code
	# tryVariableMapping(line_to_fix.strip(),buggedVariables, lines, codeToEdit)
	#############################################################


if __name__ == "__main__":
    main()