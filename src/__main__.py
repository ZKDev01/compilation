from core.scanner import build_lexer, tokenizer
from core.parser import parse, build_parser
import os

def load_tests():
    files = os.listdir('./tests/')
    files = [file for file in files if file.endswith('.hulk')]

    tests = []
    for file in files:
        with open(f'./tests/{file}', 'r') as test:
            tests.append((file, test.read()))

    return tests

if __name__ == '__main__':
    tests = load_tests()
    lexer = build_lexer()
    parser = build_parser()

    for name, test in tests:
        print(f'Running test {name}')
        tokens = tokenizer(lexer, test)
        ast = parse(parser, tokens)
        print(ast)
        print()

