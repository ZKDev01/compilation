from core.lexer import generate_lexer, tokenizer
from core.parser import parse, build_parser
from core.grammar import G
import os

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
  lexer = generate_lexer()
  parser = build_parser()
  
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

