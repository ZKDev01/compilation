class Token:
  """Basic token class. 
    
  Parameters
  ----------
  lex : str
    Token's lexeme.
  token_type : Enum
    Token's type.
  """
    
  def __init__(self, lex, token_type):
    self.lex = lex
    self.token_type = token_type