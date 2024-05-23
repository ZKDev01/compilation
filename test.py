from code_cp import tokenize

def test_1():
  tokens = tokenize('xyz + 6 * 9')
  print(tokens == ['xyz', '+', 6.0, '*', 9.0])

if __name__ == '__main__':
  test_1()