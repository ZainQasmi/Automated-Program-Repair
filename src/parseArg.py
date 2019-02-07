# How would I handle an input casewith list, tuple as input
import ast
from listTupleLogic import listTupleLogic


def appendArg(slice, collection, index, arguments):


	if index >= len(slice):
		return

	if slice[index] == '[':
		temp = collection.lists[index] # gives me index of ending parenthesis
		result = ast.literal_eval(slice[index:temp+1]) # converts into a list
		arguments.append(result)
		index = temp + 2
		return appendArg(slice, collection, index, arguments)

	elif slice[index] == '(':
		temp = collection.tuples[index]
		result = ast.literal_eval(slice[index:temp+1])
		arguments.append(result)
		index = temp + 2
		return appendArg(slice, collection, index, arguments)
		
	else:
		i = slice.find(',', index)
		if i is not -1:
			result = ast.literal_eval(slice[index:i])
			index = i+1
			arguments.append(result)
			return appendArg(slice, collection, index, arguments)
		else:
			result = ast.literal_eval(slice[index:])
			arguments.append(result)
			return




def logic(str): 
	text = "".join(str.split())
	reg = listTupleLogic()

	for i in range(len(text)):
		if text[i] == '[':
			reg.pushList(i)

		elif text[i] == ']':
			reg.popList(i)

		elif text[i] == '(':
			reg.pushTuple(i)

		elif text[i] == ')':
			reg.popTuple(i)


	return [reg, text]




def getArgs(str):
	[a, text] = logic(str)
	arguments = []
	appendArg(text,a,0, arguments)
	return arguments
