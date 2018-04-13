import ast
import re
import nltk
import tokenize, token
from itertools import permutations
from itertools import combinations
import string
import keyword

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
b5 = 'y<z'
b6 = 'stfu'
# b0 = 'for i in range(a,b):'

b6 = """breakAtIter -=1
		tempLine = line_to_fix
		print tempLine
		print oneList
		for i in range(0,len(buggedVarList)):
			temp = '([^\w\D]*\\b' + buggedVarList[i] + '\\b)|([^\w\D]*' + buggedVarList[i] + '[_\d]+)'
			tempLine = re.sub(temp, oneList[i], tempLine)
			print buggedVarList[i], ' ', oneList[i], ' ', tempLine
			counter +=1 """


with open('pipelined.py', 'r') as myfile:
	source=myfile.read()
	root = ast.parse(source)
	vars = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
print vars

def get_buggyLine_operators(line):
	operators = []
	for t in tokenize.generate_tokens(iter([line]).next):
		# print (token.tok_name[t[0]])
		if token.tok_name[t[0]] == 'NAME':
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


ops = get_buggyLine_operators(b6)
op_combinations = get_list_of_all_operator_combiantions(b6,ops)
corrected_lines = generate_new_lines_with_all_operator_combinations(b6,ops,op_combinations)
print 
print ops
# print op_combinations
# print corrected_lines

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

print
print set((intersection(ops,vars)))
print 
print(keyword.kwlist)