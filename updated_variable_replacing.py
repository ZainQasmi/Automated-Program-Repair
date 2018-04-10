import ast
import re
import nltk
import tokenize, token
from itertools import permutations
from itertools import combinations
import string

# o1 = ['+','-','*','/','%','**','//'] #arithematic ** //
o1 = ['+','-','*','/','%','**'] #arithematic ** //
# o2 = ['==','!=','<>','<','>','>=','<='] #comparison 
o2 = ['==','!=','<','>','>=','<='] #comparison 
# o3 = ['=','+=','-=','*=','/=','%=','**=','//='] #assignment ,'**=','//='
o3 = ['=','+=','-=','*='] #assignment ,'**=','//='
o4 = o1+o2+o3

abc_list = list(string.ascii_uppercase)

b1 = 'a<2'
b2 = 'a=b**c-2'
b3 = 'a+=2'
b4 = 'a//=2+4'

def get_buggyLine_operators(line):
	operators = []
	for t in tokenize.generate_tokens(iter([line]).next):
	    if token.tok_name[t[0]] == 'OP':
	    	operators.append(t[1])

	return operators

def get_list_of_all_operator_combiantions(line,operators):
	tempOpList = []
	numberOp = len(ops)
	for c in combinations(o4, numberOp):
			for p in permutations(c):
				tempOpList.append(p)

	## all possible combinations of operators generated
	return tempOpList

def generate_new_lines_with_all_operator_combinations(line,operators,operator_combinations):
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


ops = get_buggyLine_operators(b2)
op_combinations = get_list_of_all_operator_combiantions(b2,ops)
corrected_lines = generate_new_lines_with_all_operator_combinations(b2,ops,op_combinations)

