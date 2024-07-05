import os

from core.grammar import G

from core.lexer import build_lexer, tokenizer

from tools.parsers import LR1Parser
from tools.cmp.utils import Token
from tools.cmp.evaluation import evaluate_reverse_parse
from tools.semantic import SemanticCheckerVisitor, TypeCheckingVisitor

def parse(tokens: list[Token]):
  parse = LR1Parser(G)
  result = parse(tokens, get_shift_reduce=True)

  right_parse, operations = result
  ast = evaluate_reverse_parse(right_parse, operations, tokens)
  return ast

def load_tests():
  files = os.listdir('./tests/')
  files = [file for file in files if file.endswith('.hulk')]

  tests = []
  for file in files:
    with open(f'./tests/{file}', 'r') as test:
      tests.append((file, test.read()))

  return tests

def main() -> None:
  tests = load_tests()
  lexer = build_lexer()

  semantic_checker = SemanticCheckerVisitor()
  typer_checker = TypeCheckingVisitor()

  print("TESTING IN PROCESS")
  for name, test in tests:
    
    print('================= FILENAME ====================')
    print(f'file: {name}')

    print('=================== CODE ======================')
    print(f'\n\n{test}\n\n')
    
    print('================== TOKENS =====================')
    tokens = tokenizer(test, lexer=lexer)
    print(tokens)
    
    print('=================== AST =======================')
    ast = parse(tokens)
    print(ast)
    
    print('=========== SEMANTIC CHECKING =================')
    semantic_checker.clean_errors()
    semantics_errors = semantic_checker.visit(ast)
    
    print(semantics_errors)
    for i, error in enumerate(semantics_errors, 1):
      print(f'{i}.', error) 
    
    if len(semantics_errors) == 0:
      types_errors = typer_checker.visit(ast)
      print(types_errors)

if __name__ == '__main__':
  main()

