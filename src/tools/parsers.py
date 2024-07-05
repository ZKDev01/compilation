from tools.cmp.pycompiler import *
from tools.cmp.automata import State, lr0_formatter, multiline_formatter
from tools.cmp.utils import ContainerSet, Token




def compute_local_first(firsts: dict[Symbol, ContainerSet], alpha: Sentence) -> ContainerSet:
  first_alpha = ContainerSet()

  try:
    alpha_is_epsilon = alpha.IsEpsilon
  except AttributeError:
    alpha_is_epsilon = False
    
  if alpha_is_epsilon:
    first_alpha.set_epsilon()
  else:
    for symbol in alpha:
      first_alpha.update(firsts[symbol])
      if not firsts[symbol].contains_epsilon:
        break
    else:
      first_alpha.set_epsilon()
  return first_alpha

def compute_firsts(G):
  firsts = {}
  change = True
  # init First(Vt)
  for terminal in G.terminals:
    firsts[terminal] = ContainerSet(terminal)
  # init First(Vn)
  for nonterminal in G.nonTerminals:
    firsts[nonterminal] = ContainerSet()
  while change:
    change = False
    # P: X -> alpha
    for production in G.Productions:
      X = production.Left
      alpha = production.Right
      # get current First(X)
      first_X = firsts[X]
      # init First(alpha)
      try:
        first_alpha = firsts[alpha]
      except KeyError:
        first_alpha = firsts[alpha] = ContainerSet()
      # CurrentFirst(alpha)???
      local_first = compute_local_first(firsts, alpha)
      # update First(X) and First(alpha) from CurrentFirst(alpha)
      change |= first_alpha.hard_update(local_first)
      change |= first_X.hard_update(local_first)
  # First(Vt) + First(Vt) + First(RightSides)
  return firsts

def compute_follows(G, firsts):
  follows = { }
  change = True
  
  # init Follow(Vn)
  for nonterminal in G.nonTerminals:
    follows[nonterminal] = ContainerSet()
  follows[G.startSymbol] = ContainerSet(G.EOF)
  
  while change:
    change = False
    # P: X -> alpha
    for production in G.Productions:
      X = production.Left
      alpha = production.Right
      follow_X = follows[X]
      ###################################################
      # X -> zeta Y beta
      # First(beta) - { epsilon } subset of Follow(Y)
      # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
      ###################################################
      if alpha.IsEpsilon:
        continue
            
      n = len(alpha._symbols)-1
      for i in range(n):
        Y = alpha._symbols[i]
        beta = alpha._symbols[i+1]
        if Y.IsNonTerminal:
          change |= follows[Y].update(firsts[beta])
          if firsts[beta].contains_epsilon:
            change |= follows[Y].update(follow_X)
        if i == n-1 and beta.IsNonTerminal:
          change |= follows[beta].update(follow_X)
      ###################################################
  # Follow(Vn)
  return follows


