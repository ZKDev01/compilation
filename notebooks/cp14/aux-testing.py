from grammar import G
from utils import fixed_tokens, tokenize_text, pprint_tokens
#from parsing import LR1Parser
from cmp.tools.parsing import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from visitor import FormatVisitor

from text01 import text

def testing_grammar() -> None:
  print(G)

def testing_tokens() -> None:
  tokens = tokenize_text(text)
  pprint_tokens(tokens)

def testing_parsing() -> None:
  tokens = tokenize_text(text)
  parser = LR1Parser(G=G)
  parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
  print('\n'.join(repr(x) for x in parse))

def testing_ast() -> None:
  tokens = tokenize_text(text)
  parser = LR1Parser(G=G)
  parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
  ast = evaluate_reverse_parse(parse, operations, tokens)

def testing_visitor() -> None:
  tokens = tokenize_text(text)
  parser = LR1Parser(G=G)
  parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
  ast = evaluate_reverse_parse(parse, operations, tokens)
  formatter = FormatVisitor()
  tree = formatter.visit(ast)
  print(tree)

  assert tree == '''\__ProgramNode [<class> ... <class>]
	\__ClassDeclarationNode: class A  { <feature> ... <feature> }
		\__AttrDeclarationNode: a : int
		\__FuncDeclarationNode: def suma(a:int, b:int) : int -> <body>
			\__<expr> PlusNode <expr>
				\__ VariableNode: a
				\__ VariableNode: b
		\__AttrDeclarationNode: b : int
	\__ClassDeclarationNode: class B : A { <feature> ... <feature> }
		\__AttrDeclarationNode: c : A
		\__FuncDeclarationNode: def f(d:int, a:A) : void -> <body>
			\__VarDeclarationNode: let f : int = <expr>
				\__ ConstantNumNode: 8
			\__AssignNode: let c = <expr>
				\__CallNode: <obj>.suma(<expr>, ..., <expr>)
					\__ InstantiateNode: new A()
					\__ ConstantNumNode: 5
					\__ VariableNode: f
			\__ VariableNode: c'''

if __name__ == '__main__':
  testing_grammar()
  testing_tokens()
  testing_parsing()
  testing_ast()
  testing_visitor()
  
  print("OK!")
