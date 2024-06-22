from cmp.pycompiler import *

from cmp.utils import ContainerSet

def main() -> None:
  G = Grammar()
  E = G.NonTerminal('E', True)
  T,F,X,Y = G.NonTerminals('T F X Y')
  plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

  E %= T + X
  X %= plus + T + X | minus + T + X | G.Epsilon
  T %= F + Y
  Y %= star + F + Y | div + F + Y | G.Epsilon
  F %= num | opar + E + cpar

def compute_local_first(firsts, alpha):
  first_alpha = ContainerSet()
  
  try:
    alpha_is_epsilon = alpha.IsEpsilon
  except:
    alpha_is_epsilon = False

  if alpha_is_epsilon:
    first_alpha.set_epsilon()

  else:
    first_alpha.update(firsts[alpha._symbols[0]])
    i = 0
    x_i = alpha._symbols[i]
    while firsts[x_i].contains_epsilon:
      if i == len(alpha._symbols):
        first_alpha.set_epsilon()
        break
      i += 1
      x_i = alpha._symbols[i]
      if not firsts[x_i].contains_epsilon:
        first_alpha.update(firsts[x_i])  
        break 
  
  return first_alpha

def compute_firsts(G):
  firsts = {}
  change = True

  for terminal in G.terminals:
    firsts[terminal] = ContainerSet(terminal)

  for nonterminal in G.nonTerminals:
    firsts[nonterminal] = ContainerSet()
  while change:
    change = False

    for production in G.Productions:
      X = production.Left
      alpha = production.Right
      
      first_X = firsts[X]
      
      try:
        first_alpha = firsts[alpha]
      except KeyError:
        first_alpha = firsts[alpha] = ContainerSet()
      
      local_first = compute_local_first(firsts, alpha)
      
      change |= first_alpha.hard_update(local_first)
      change |= first_X.hard_update(local_first)
  
  return firsts

if __name__ == '__main__':
  main()