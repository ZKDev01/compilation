import os

from core.grammar import G

from core.lexer import build_lexer, tokenizer
from core.parser import parse, build_parser

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

  print("TESTING IN PROCESS")
  for name, test in tests:
    
    print('================= FILENAME ====================')
    print(f'file: {name}')

    print('=================== CODE ======================')
    print(f'\n\n{test}\n\n')
    
    print('================== TOKENS =====================')
    tokens = tokenizer(test, lexer=lexer)
    print(tokens)
    
    print('==================== AST ======================')
    ast = parse(tokens)
    print(ast)

if __name__ == '__main__':
  main()

