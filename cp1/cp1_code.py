from cp1_utils import BadEOFError, ParsingError, is_int, is_float, apply, find_parentheses_index, order_evaluate
from cp1_hulk import constants, elemental_functions, operations

def tokenize(text: str) -> list:
  """Basic Tokenizer
  Returns the set of tokens. 
  At this point, simply splits by spaces and converts numbers to `float` instances.
  Also recognizes the language's constants

  Args:
      text (str): text to tokenize
  
  Returns:
      list: result applying the tokenization process
  """
  tokens = []
  for item in text.split(' '):
    if is_float(item):
      item = float(item)
    if item in constants:
      item = constants[item]
    tokens.append(item)
  return tokens    

def get_token(tokens, i, error_type=BadEOFError):
  """
  Returns tokens[i] if 'i' is in range. Otherwise, raises ParsingError exception.
  """
  try:
    return tokens[i]
  except IndexError:
    raise error_type()

def evaluate(tokens):
  """
  Evaluates an expression recursively.
  """
  i, value = parse_expression(tokens, 0, len(tokens))
  # if all tokens were analyzed
  if i == len(tokens):
    return value
  raise ParsingError

def parse_expression(tokens, i, count):
  """Recursive Function

  Busca los terminos '(' ')' para ir a parse_term y evaluarlo en dependencia de los operadores y las funciones elementales

  Args:
      tokens (_type_): _description_
      i (_type_): _description_
  """
  if i == count:
    return count, tokens[0]
  else: 
    exist, first, last = find_parentheses_index(tokens)
    if exist:
      # TODO
      return parse_expression(tokens, i, count)
    if (first == -1 and last != -1) or (first != -1 and last == -1):
      return i, tokens[0]
    raise ParsingError

def parse_term(tokens, i):
  """Parse binary term 

  Funcion para las reglas de los operadores
  
  Args:
      tokens (_type_): apply tokenize an str
      i (_type_): index term {binary op or func}

  Raises:
      ParsingError: _description_

  Returns:
      _type_: expression and analyzed tokens 
  """

  # TODO: este metodo para lograr un orden a la hora de la evaluacion, primero reconociendo las funciones elementales y modificar los tokens evaluando primero las funciones elementales
  term, typedef = order_evaluate(tokens)
  if typedef == 'ef':
    pass
  

  # TODO: luego de evaluar las funciones elementales usar 'eval()' para evaluar la expresion 
  # HASTA AQUI EVALUA
  term = tokens[i]
  left_value = tokens[i-1]
  right_value = tokens[i+1]
  del tokens[i+1]
  del tokens[i]
  if term in operations:
    term = operations[term]
    tokens[i-1] = term(left_value, right_value)
    return tokens, 3
  if term in elemental_functions:
    term = elemental_functions[term]
    tokens[i-1] = term(left_value, right_value)
    return tokens, 3
  raise ParsingError

class Testing_Code_CP1:
  def testing_code_1():
    tokens = [7, '+', 3]
    count = len(tokens)
    analized = 0
    i = 1
    tokens, i = parse_term(tokens, i)
    results = f"""
    tokens: {tokens}
    analyzed tokens: {analized + i}
    total tokens: {count}
    """
    print(results)
  def testing_code_2():
    expression = '(50 + (401 + e + (1 + 1)))'
    first, last = find_parentheses_index(expression)
    expression = tokenize(expression)
    results = f"""
    first: {first}
    last: {last}
    reduce expression: {expression[first, last]}
    """
    print(results)

if __name__ == '__main__':
  # Testing_Code_CP1.testing_code_1()
  
  tokens = tokenize('log ( 64 , 1 + 3 )')
  print(order_evaluate(tokens))

