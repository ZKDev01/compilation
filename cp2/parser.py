from exception_handling import ParsingError

class Parser:
  """
  Base parser class.
  """
    
  def __init__(self):
    self.lexer = None
    self.left_parse = None
    self.lookahead = None
        
  def parse(self, lexer):
    """
    Returns a left parse given the tokens from the lexer.
    """
    try:
      self.lexer = lexer
      self.left_parse = []
      self.lookahead = lexer.next_token().token_type
      self.begin()
      return self.left_parse
        
    except ParsingError as error:
      print(f'Parsing error: {error}!!!')
      print(f'Lookahead: {self.lookahead}')
      print(f'Unfinished parse: {self.left_parse}')
            
    finally:
      self.lex = None
      self.left_parse = None
      self.lookahead = None
            
  def begin(self):
    """
    Begin parsing from starting symbol and match EOF.
    """
    raise NotImplementedError()
        
  def report(self, production):
    """
    Adds production to the left parse that is being build.
    """
    self.left_parse.append(production)
        
  def error(self, msg=None):
    """
    Raises a parsing error.
    """
    raise ParsingError(msg)
        
  def match(self, token_type):
    """
    Consumes one token from the lexer if lookahead matches the given token type.
    Raises parsing error otherwise.
    """
    if token_type == self.lookahead:
      try:
        self.lookahead = self.lexer.next_token().token_type
      except AttributeError:
        self.lookahead = None
      else:
        self.error('Unexpected token')