from cp1_utils import BadEOFError, ParsingError, is_int, is_float
from hulk import constants, functions, operations

def tokenize(text: str) -> list:
  """Basic Tokenizer
  Returns the set of tokens. At this point, simply splits by 
  spaces and converts numbers to `float` instances.

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

  print(tokens)
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
  try:
    i, value = parse_expression(tokens, 0)
    assert i == len(tokens)
    return value
  except ParsingError as error:
    print(error)
    return None

# RESTRICCION: Sin usar ciclos
def parse_expression(tokens, i):
  i, term = parse_term(tokens, i)
  if i < len(tokens):
    if tokens[i] == '+':
    # Insert your code here ...
      pass
  return i, term
        
def parse_term(tokens, i):
  # Insert your code here ...
  pass

def parse_factor(tokens, i):
  # Insert your code here ...
  pass

"""
Agreguemos constantes numéricas al lenguaje `HULK` 
Para ello, simplemente añadiremos un diccionario con 
todas las constantes disponibles, que usaremos durante 
la tokenización. Nótese que solo es necesario modificar 
el _lexer_ para añadir este rasgo al lenguaje.

Agreguemos funciones elementales `sin`, `cos`, `tan`, `log`, 
`sqrt`, etc. El llamado a funciones se hará en notación 
prefija, comenzando por el nombre de la función y seguido, 
entre paréntesis, por los argumentos, que estarán separados 
entre sí por _comas_.

Para las funciones elementales haremos algo similar a las 
constantes, pero en vez de a la hora de tokenizar, las 
reemplazaremos a la hora de evaluar, pues necesitamos
evaluar recursivamente los argumentos de la función. 
Empezaremos por garantizar que nuestro tokenizador que es 
capaz de reconocer expresiones con funciones elementales 
de más de un argumento, en caso de no ser así es necesario 
arreglarlo.

Por último, modificaremos el método `evaluate` para que use
las funciones elementales. Recordemos que los argumentos 
están separados por el token _coma_ (`,`) y que cada uno 
puede a su vez tener sub-expresiones que consistan también 
en llamados a funciones.
"""
