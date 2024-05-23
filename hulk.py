import math

operations = {
  '+': lambda x,y: x + y,
  '-': lambda x,y: x - y,
  '*': lambda x,y: x * y,
  '/': lambda x,y: x / y,
}
constants = {
  'pi': 3.14159265359,
  'e': 2.71828182846,
  'phi': 1.61803398875,
}
functions = {
  'sin': lambda x: math.sin(x),
  'cos': lambda x: math.cos(x),
  'tan': lambda x: math.tan(x),
  'log': lambda x,y: math.log(x, y),
  'sqrt': lambda x: math.sqrt(x),
}

if __name__ == "__main__":
  item = 'pi'
  print(item in constants)
  print(constants[item])

  for item in constants:
    text = f"""
    item: {item}
    """
    # print(text)