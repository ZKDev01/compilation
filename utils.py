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
