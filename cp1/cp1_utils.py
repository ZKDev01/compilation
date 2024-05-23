from cp1_hulk import operations, elemental_functions

def is_int(text: str) -> bool:
  try:
    int(text)
    return True
  except ValueError:
    return False
def is_float(text: str) -> bool:
  try:
    float(text)
    return True
  except ValueError:
    return False
def apply(op, left_value, right_value):
  try: 
    op = operations[op]
    return op(left_value, right_value)
  except Exception as e:
    print(f"{e}")
def find_parentheses_index(tokens: list):
  first_close = -1
  last_open = -1
  for i in range(0, len(tokens)): 
    if tokens[i] == '(':
      last_open = i
    if tokens[i] == ')':
      first_close = i
      break
  return (last_open != -1 and first_close != -1), last_open, first_close
def order_evaluate(tokens: list):
  # TODO: la funcion debe ser capaz de identificar la lista de funciones elementales y devolver su funcion lambda, sino, devolver que solo quedan o operadores o no queda nada
  if any(value for key, value in elemental_functions.items() if key in tokens):
    return next(iter( [key for key in elemental_functions.keys() if key in tokens] ), None)
  return None

class ParsingError(Exception):
  """
  Base class for all parsing exceptions.
  """
  pass

class BadEOFError(ParsingError):
  """
  Unexpected EOF error.
  """  
  def __init__(self):
    ParsingError.__init__(self, "Unexpected EOF")

class UnexpectedToken(ParsingError):
  """
  Unexpected token error.
  """
  def __init__(self, token, i):
    ParsingError.__init__(self, f'Unexpected token: {token} at {i}')

class MissingCloseParenthesisError(ParsingError):
  """
  Missing ')' token error.
  """
  def __init__(self, token, i):
    ParsingError.__init__(self, f'Expected ")" token at {i}. Got "{token}" instead')

class MissingOpenParenthesisError(ParsingError):
  """
  Missing '(' token error.
  """
  def __init__(self, token, i):
    ParsingError.__init__(self, f'Expected "(" token at {i}. Got "{token}" instead')

if __name__ == "__main__":
  tokens = [ '(', 5, '+', 5, ')' ]
  boolean, first, last = find_parentheses_index(tokens)
  results = f"""
  Find indexs: {boolean}
  First index: {first}
  Token: {tokens[first]}
  Last index: {last}
  Token: {tokens[last]}
  Reduce: {tokens[first+1: last]}
  """
  print(results)