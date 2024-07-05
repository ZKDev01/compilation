from tools.cmp.utils import Token
from tools.parsers import LR1Parser
from core.scanner import build_lexer, tokenizer
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
  lexer = build_lexer()
  # parser = build_parser()
  
  print("TESTING IN PROCESS")
  for _, test in tests:
    tokens = tokenizer(test, lexer=lexer)
    print("========= TOKENS ===========")
    print(tokens)
    #ast = parse(parser, tokens)
    #print(ast)
    print()

if __name__ == '__main__':
  main()

