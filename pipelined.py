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
from blocks_DJ import *

### Writes test filename and test result filename to file which will be used by tarantula.py
with open("importNames.csv", "w") as text_file:
    text_file.write("%s,%s" %(sys.argv[1],sys.argv[2])) 

### Executes tarantula which isolates the bugged line and stores it in list lines. 
### The line with highest likelihood of having a bug is at first index i.e. lines[0]
print '//===-------------------- Running Tarantula ---------------------===//'
execfile('tarantula.py')
print '//===----------------------- Returns Tarantula ------------------------===//'

print
buggedLine = lines[0].lineNo
print '//===--------------------    Bugged Line    ---------------------===//'
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
	tempCodeString = ''
	abc_list = list(string.ascii_uppercase)
	new_lines = generate_new_lines_with_all_variable_combinations(line_to_fix, buggedVarList, suggestedVarListofLists)

	for temp_line in new_lines:
		# print "2:",temp_line, line_to_fix
		tabsToAdd =  len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip()) ## Calculate and add requisite no. of tabs to the changed line of code

		for i in range (0,tabsToAdd):
			temp_line = '\t' + temp_line
		codeToEdit[buggedLine-1] = temp_line

		for line in codeToEdit:
			tempCodeString += line + '\n'

		if testRepairedCode.unittests(tempCodeString):
			print '//===--------------- VAR: Start Code with Bug Fix ---------------===//'
			print tempCodeString
			print '//===---------------- VAR: End Code with Bug Fix ----------------===//'

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
	return tempOpList ## All possible combinations of operators generated

def tryOperatorReplacement(line_to_fix, buggedOperators, suggestedOperatorListofLists, codeToEdit, original_code):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically

	tempCodeString = ''
	abc_list = list(string.ascii_uppercase)
	new_lines = generate_new_lines_with_all_operator_combinations(line_to_fix, buggedOperators, suggestedOperatorListofLists)
	
	for temp_line in new_lines:
		# print "1:",temp_line, line_to_fix
		tabsToAdd =  len(codeToEdit[buggedLine-1]) - len(codeToEdit[buggedLine-1].lstrip()) ## Calculate and add requisite no. of tabs to the changed line of code

		for i in range (0,tabsToAdd):
			temp_line = '\t' + temp_line
		codeToEdit[buggedLine-1] = temp_line

		for line in codeToEdit:
			tempCodeString += line + '\n'

		if testRepairedCode.unittests(tempCodeString):
			print '//===------------------------ OPR: Start Code with Bug Fix -----------------------===//'
			print tempCodeString
			print '//===------------------------- OPR: End Code with Bug Fix -----------------------===//'

def tryVariableMapping(line_to_fix, buggedVarList, p_lines, codeToEdit):
	exec('import %s as testRepairedCode'%sys.argv[3]) # Import Test Module Dynamically

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
			print '//===------------ Blocks: Start code with Bug Fix --------------===//'
			print tempCodeString
			print '//===------------- Blocks: End code with Bug Fix --------------===//'

def generate_new_lines_with_all_variable_combinations(line_to_fix,buggedVarList,operator_combinations):
	return generate_new_lines_with_all_operator_combinations(line_to_fix,buggedVarList,operator_combinations)

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

	temp_line = line_to_fix.strip()
	if line_to_fix[len(line_to_fix)-1] == ':':
		temp_line = line_to_fix.strip() + 'pass'

	############################################################
	# before passing codeToEdit in each function. make codeToEdit=Original_bugged_code. Here original_bugged_code is mid.py in 
	#its original incorrect. Otherwise there are problelms

	# update codeToEdit after every function call. Therefore I have introduced the back_up_code variable, which
	# contains the original incorrect state of mid.py
	back_up_code = codeToEdit
	buggedVariables = makeVarList(temp_line)
	suggestedVarListofLists = makeVarCombination(totalVariables, len(buggedVariables))
	tryVariableReplacement(line_to_fix.strip(),buggedVariables,suggestedVarListofLists, codeToEdit, original_code)
	codeToEdit = back_up_code
	buggedOperators = get_buggyLine_operators(line_to_fix.strip())
	suggestedOperatorListofLists = get_list_of_all_operator_combinations(line_to_fix.strip, buggedOperators)
	tryOperatorReplacement(line_to_fix.strip(), buggedOperators, suggestedOperatorListofLists, codeToEdit, original_code )
	codeToEdit = back_up_code
	tryVariableMapping(line_to_fix.strip(),buggedVariables, lines, codeToEdit)
	#############################################################


if __name__ == "__main__":
    main()