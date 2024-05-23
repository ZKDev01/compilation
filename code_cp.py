from utils import is_int, is_float

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
    tokens.append(item)
  return tokens    