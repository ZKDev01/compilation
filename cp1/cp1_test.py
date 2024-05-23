from cp1_code import tokenize, evaluate

def test_tokenize():
  assert tokenize('7 + 6 * 9') == [7.0, '+', 6.0, '*', 9.0]
  assert tokenize('log ( 64 , 1 + 3 )') == ['log', '(', 64.0, ',', 1.0, '+', 3.0, ')']
  assert tokenize('2 * pi') == [2.0, '*', 3.14159265359]

def test_evaluate():
  assert evaluate(tokenize('5 + 6 * 9')) == 59.
  assert evaluate(tokenize('( 5 + 6 ) * 9')) == 99.
  assert evaluate(tokenize('2 * pi')) == 6.28318530718
  assert evaluate(tokenize('( 5 + 6 ) + 1 * 9 + 2')) == 22.
  assert evaluate(tokenize('1 - 1 + 1')) == 1
  assert evaluate(tokenize('8 / 4 / 2')) == 1

if __name__ == '__main__':
  test_tokenize()
  # test_evaluate()