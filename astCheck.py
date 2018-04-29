# import asttokens


File = open("mid.py","r")
source= File.read()
source= ('a=0')

# # st='def foo():\n    """\n    Test\n    """'
# atok = asttokens.ASTTokens(st, parse=True)
# print atok.tree.body[0].first_token.start[0]
# print atok.tree.body[0].body[0].first_token.start[0]


# =================================================================

# source = '''
# class Foo(object):
#     def setUp(self):
#         self.var1 = "some value"
#         self.var2 = 1
#     def bar(self):
#         var3 = 2
#     def baz(self, var):
#         var4 = var
# '''

import ast

def hack(source):
    root = ast.literal_eval(source)

    for node in ast.walk(root):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            yield node.id
            print node.id
        elif isinstance(node, ast.Attribute):
            yield node.attr
            print node.attr
        elif isinstance(node, ast.FunctionDef):
            yield node.name
            print node.literal_eval

print(list(hack(source)))

# from logilab.astng.builder import ASTNGBuilder
# builder = ASTNGBuilder()
# astng = builder.string_build('i = 1', __name__, '<string>')
# assnode = astng['']
# print [(inf.value, type(inf.value)) for inf in assnode.infer()]