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
