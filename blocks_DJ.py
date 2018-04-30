from comparisons import *
import keyword
import nltk
import tokenize, token
import collections
from itertools import permutations
from itertools import combinations
import numpy as np
import csv
from os.path import splitext

def get_buggyLine_operators(line):
	operators = []
	for t in tokenize.generate_tokens(iter([line]).next):
	    if token.tok_name[t[0]] == 'NAME':
	    	operators.append(t[1])

	return operators

def loadScript(fname,lines):
    with open(fname) as f:
        for i, l in enumerate(f):
			lines.append(l)
    return i + 1


def makeVarCombination(totalVariables, lenBuggedVars):
	tempVarList = []
	for c in combinations(totalVariables, lenBuggedVars):
		for p in permutations(c):
			tempVarList.append(p)
	return tempVarList

block_size = 3
buggedLineNo = 7

lines = []
blocks_list = []


f = open('importNames.csv', 'rb')
reader = csv.reader(f)
for row in reader:
	print row[0]
	testFileName = row[0]
	resultsFileName = row[1]
f.close()

loadScript(testFileName, lines)

for i in range(0,len(lines)):
	if (i+2 < len(lines)):
		if i >= buggedLineNo-block_size and i <= buggedLineNo-4+block_size:
			continue
		else:
			blocks_list.append(lines[i]+lines[i+1]+lines[i+2])

buggy_block = lines[5]+lines[6]+lines[7]
key_word = keyword.kwlist + [splitext(testFileName)[0]]
key_word = set(key_word)
l_dist = {}
l_dist_vars = {}

for i in range(0,len(blocks_list)):
	bb_vars = set(get_buggyLine_operators(blocks_list[i]))
	bb_vars = list(bb_vars - key_word)
	l_dist[levenshtein_distance.compare(buggy_block,blocks_list[i])] = blocks_list[i]
	l_dist_vars[levenshtein_distance.compare(buggy_block,blocks_list[i])] = bb_vars

similarities = l_dist.keys()
similarities = sorted(similarities,reverse = True)

if len(similarities) > 3:
	similarities = similarities[:3]

temp_vars = []
for i in similarities:
	# print "similarity: " + str(i) + "\n" + str(l_dist[i])
	temp_vars.append(l_dist_vars[i])
	# print "variables: " + str(l_dist_vars[i]) + "\n"
	# print "//////////////////////////////////////////"


# print "\n\n++++++++\n\n"
# for v_list in temp_vars:
# 	print makeVarCombination(v_list,2)
