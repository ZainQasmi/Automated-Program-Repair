# import tokenize

# with open('testing2.py', 'rb') as f:
# 	a = tokenize.tokenize(f.readline)
# 	print a
#     # for five_tuple in tokenize.tokenize(f.readline):
#         # print five_tuple
#         # print(five_tuple.type)
#         # print(five_tuple.string)
#         # print(five_tuple.start)
#         # print(five_tuple.end)
#         # print(five_tuple.line)


import tokenize, token

# s = "{'test':'123','hehe':['hooray',0x10]}"
b1 = 'a<<2'
b2 = 'a=b+c-*'
b3 = 'a+=2'
b4 = 'a//2'

for t in tokenize.generate_tokens(iter([b2]).next):
	# print t
	if token.tok_name[t[0]] == 'NAME':
		print t[1]