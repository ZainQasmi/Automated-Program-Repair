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
from comparisons import *
import keyword
import nltk
from blocks_DJ import *

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
def tryOperatorsReplacement(line_to_fix, codeToEdit):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically
	
	tempLine = line_to_fix
	tempCodeString = ''
	ops = get_buggyLine_operators(line_to_fix)
	op_combinations = get_list_of_all_operator_combinations(line_to_fix,ops)
	# corrected_lines has all possible lines that can be generated from the bugged line with replaced operators
	corrected_lines = generate_new_lines_with_all_operator_combinations(line_to_fix,ops,op_combinations)
	
	for each_line in corrected_lines:
		# now we pick each newly generated line from corrected_lines
		tabsToAdd = len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())
	
		for i in range(0,tabsToAdd):
			each_line = '\t' + each_line

		# after adding all the tabs, etc in the new line
		# we insert that line in the main function code
		codeToEdit[buggedLine-1] = each_line


		# tempCodeString has a new variant of the original_function in each iteration of the loop
		for line in codeToEdit:
			tempCodeString += line + '\n'

		# we check each new variant one by one against all the test cases
		# This if statement will only be valid if code is fixed through operato replacement
		if testRepairedCode.unittests(tempCodeString):
			print '//===------------------------ Code with Bug Fix through Operator Replacement-----------------------===//'
			print tempCodeString


def tryVariableMapping(line_to_fix, buggedVarList, p_lines, codeToEdit):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically
	# we have yet to make the block size a variable. Currently it is fixed to 3 I think.
	# This needs to be corrected

	#############################
	# block_size = 3 
	#############################

	# blocks_list = []

	# for i in range(0,len(p_lines)):
	# 	if (i+2 < len(p_lines)):
	# 		if i >= buggedLine-block_size and i <= buggedLine-4+block_size:
	# 			continue
	# 		else:
	# 			blocks_list.append(p_lines[i]+p_lines[i+1]+p_lines[i+2])
		
	# buggy_block = p_lines[buggedLine-2] + p_lines[buggedLine-1] + p_lines[buggedLine]

	#############################
	# The function name must be inserted in the key_word list dynamically
	# here we are explicitly adding 'mid' as the keyword
	# key_word = keyword.kwlist + ['mid']
	#############################

	# key_word = set(key_word)
	# leven_dist_blocks = {}
	# leven_dist_blocks_variables = {}

	# for i in range(0,len(blocks_list)):

	# 	buggy_block_vars = set(get_buggyLine_operator_names(blocks_list[i]))
	# 	buggy_block_vars = list(buggy_block_vars - key_word)
	# 	leven_dist_blocks[levenshtein_distance.compare(buggy_block,blocks_list[i])] = blocks_list[i]
	# 	leven_dist_blocks_variables[levenshtein_distance.compare(buggy_block,blocks_list[i])] = buggy_block_vars
		
	#print levenshtein_distance.compare("dawood","dawood")
	#print leven_dist_blocks
	
	l_distances = l_dist.keys()
	l_distances = sorted(l_distances, reverse = True)

	if len(l_distances) > 3:
		l_distances = l_distances[:3]

	block_vars = []
	for i in l_distances:
		block_vars.append(l_dist_vars[i])

	all_combs = []
	for var_list in block_vars:
		v_combinations = makeVarCombination(var_list,len(buggedVarList))
		for each_comb_list in v_combinations:
			all_combs.append(each_comb_list)

	
	all_combs = list(set(all_combs))
	
	#print all_combs
	corrected_lines = generate_new_lines_with_all_variable_combinations(line_to_fix,buggedVarList,all_combs)
	#print corrected_lines

	for each_line in corrected_lines:
		tempCodeString = ''
		tabsToAdd = len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip())
	
		for i in range(0,tabsToAdd):
			each_line = '\t' + each_line

		codeToEdit[buggedLine-1] = each_line

		for line in codeToEdit:
			tempCodeString += line + '\n'

		
		if testRepairedCode.unittests(tempCodeString):
			print '//===------------------------ Code with Bug Fix through Blocks Mapping-----------------------===//'
			print tempCodeString
		
def generate_new_lines_with_all_variable_combinations(line_to_fix,buggedVarList,operator_combinations):
	return generate_new_lines_with_all_operator_combinations(line_to_fix,buggedVarList,operator_combinations)

def tryVariableReplacement(line_to_fix, buggedVarList, suggestedVarListofLists, codeToEdit, original_code):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically
	
	# print 'line actual: ',line_to_fix
	# print buggedVarList
	tempLine = line_to_fix
	tempCodeString = ''
	counter = 0;

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
			print '//===------------------------ Code with Bug Fix through Variable Replacement-----------------------===//'
			print tempCodeString

		# testRepairedCode(tempCodeString, original_code)
	# print counter

def testRepairedCode(tempCodeString, original_code):
	pass
	# exec('%s.unittests(tempCodeString)'%sys.argv[3])
	# exec('import %s as testRepairedCode'%sys.argv[3])
	# print testRepairedCode.unittests(tempCodeString)
	# funName2 = 'testMid.unittests(tempCodeString)'
	# exec(funName2)	
	# exec('%s(*(tests[i]))' % funName)
	
	# exec('''loadtestcases.txt''' % funName)
	# if testMid.tests(tempCodeString):
		# print tempCodeString

	# print mid(2,1,3)
	# potentiallyCorrect = True

	# for oneCase in testCaseResuts:

	# 	strInput = oneCase[0]
	# 	tupleofIntCastedInput = tuple(map(int, strInput.split(',')))
		
	# 	exec(original_code)
	# 	originalCodeOutput = mid(*tupleofIntCastedInput)
	# 	# print 'ori', originalCodeOutput

	# 	exec(tempCodeString)
	# 	suggestedCodeOutput = mid(*tupleofIntCastedInput)
	# 	# print 'sug', originalCodeOutput, tempCodeString

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
	# 		pass
	# 	print oneCase, suggestedCodeOutput, originalCodeOutput
		# print 'sug', suggestedCodeOutput
	# print "Function returns ::",suggestedCodeOutput

def get_buggyLine_operator_names(line):
	operators = []
	for t in tokenize.generate_tokens(iter([line]).next):
	    if token.tok_name[t[0]] == 'NAME':
	    	operators.append(t[1])

	return operators


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
	

	# line_to_fix = 'a=b**c-2'


	############################################################3
	# before passing codeToEdit in each function. make codeToEdit=Original_bugged_code. Here original_bugged_code is mid.py in 
	#its original incorrect. Otherwise there are problelms

	# update codeToEdit after every function call. Therefore I have introduced the back_up_code variable, which
	# contains the original incorrect state of mid.py
	back_up_code = codeToEdit
	tryVariableReplacement(line_to_fix.strip(),buggedVariables,suggestedVarListofLists, codeToEdit, original_code)
	codeToEdit = back_up_code
	tryOperatorsReplacement(line_to_fix.strip(), codeToEdit)
	code = back_up_code
	tryVariableMapping(line_to_fix.strip(),buggedVariables, lines, codeToEdit)
	#############################################################

	# print ops
	# for op in op_combinations:
		# print op[0]
	# for oneLiner in corrected_lines:
	# 	print oneLiner
	# print line_to_fix.strip()


if __name__ == "__main__":
    main()
