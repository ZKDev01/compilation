class Lexer:
  """Base lexer class.
  
  Parameters
  ----------
  text : str
    String to tokenize.
  """

  def __init__(self, text):
    self.index = 0
    self.text = text
    self.tokens = self.tokenize_text()
    
  def tokenize_text(self):
    """
    Tokenize `self.text` and set it to `self.tokens`.
    """
    raise NotImplementedError()
    
  def next_token(self):
    """
    Returns the next tokens readed by the lexer. `None` if `self.tokens` is exhausted.
    """
    try:
      token = self.tokens[self.index]
      self.index += 1
      return token
    except IndexError:
      return None
    
  def is_done(self):
    """
    Returns whether or not `self.tokens` is exhausted.
    """
    try:
      self.tokens[self.index]
      return False
    except IndexError:
      return True