from cmp.utils import ContainerSet
from cmp.automata import State, multiline_formatter
from cmp.pycompiler import Item
from grammar import G

# Computes First(alpha), given First(Vt) and First(Vn) 
# alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha):
  first_alpha = ContainerSet()
  
  try:
    alpha_is_epsilon = alpha.IsEpsilon
  except:
    alpha_is_epsilon = False
  
  ###################################################
  # alpha == epsilon => First(alpha) = { epsilon }
  ###################################################
  #                   <CODE_HERE>                   #
  ###################################################
  if alpha_is_epsilon:
    first_alpha.set_epsilon()
  ###################################################
  # alpha = X1 ... XN
  # First(Xi) subconjunto First(alpha)
  # epsilon pertenece a First(X1)...First(Xi) => First(Xi+1) subconjunto de First(X) y First(alpha)
  # epsilon pertenece a First(X1)...First(XN) => epsilon pertence a First(X) y al First(alpha)
  ###################################################
  #                   <CODE_HERE>                   #
  ###################################################
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
  ###################################################
  # First(alpha)
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

  local_firsts = {}
  
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
      #                   <CODE_HERE>                   #
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

def expand(item, G):
  next_symbol = item.NextSymbol
  if next_symbol is None or not next_symbol.IsNonTerminal:
    return []
    
  lookaheads = ContainerSet()
  firsts = compute_firsts(G)
  firsts[G.EOF] = ContainerSet(G.EOF)
  # Compute lookahead for child items
  for preview in item.Preview():
    lookaheads.update(compute_local_first(firsts,preview))        
    
  assert not lookaheads.contains_epsilon
  # Build and return child items
  output = []
  for production in G.Productions:
    if production.Left == next_symbol:
      output.append(Item(production,0,lookaheads))
  return output

def compress(items):
  centers = {}

  for item in items:
    center = item.Center()
    try:
      lookaheads = centers[center]
    except KeyError:
      centers[center] = lookaheads = set()
    lookaheads.update(item.lookaheads)
    
  return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
  closure = ContainerSet(*items)
    
  changed = True
  while changed:
    changed = False
        
    new_items = ContainerSet()
    for item in closure:
      for new_item in expand(item,G):
        new_items.add(new_item)  

    changed = closure.update(new_items)
  return compress(closure)

def goto_lr1(items, symbol, G, just_kernel=False):
  #assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
  items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
  return items if just_kernel else closure_lr1(items, G)

def build_LR1_automaton(G):
  assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
  # firsts = compute_firsts(G)
  # firsts[G.EOF] = ContainerSet(G.EOF)
    
  start_production = G.startSymbol.productions[0]
  start_item = Item(start_production, 0, lookaheads=(G.EOF,))
  start = frozenset([start_item])
    
  closure = closure_lr1(start, G)
  automaton = State(frozenset(closure), True)
    
  pending = [ start ]
  visited = { start: automaton }
    
  while pending:
    current = pending.pop()
    current_state = visited[current]
        
    for symbol in G.terminals + G.nonTerminals:
      # Get/Build `next_state`
      next_items = frozenset(goto_lr1(current_state.state,symbol,G))
      if not next_items:
        continue
      try:
        next_state = visited[next_items]
      except KeyError:
        visited[next_items] = State(next_items,True)
        pending.append(next_items)
        next_state = visited[next_items]
            
      current_state.add_transition(symbol.Name, next_state)
    
  automaton.set_formatter(multiline_formatter)
  return automaton

class ShiftReduceParser:
  SHIFT = 'SHIFT'
  REDUCE = 'REDUCE'
  OK = 'OK'
    
  def __init__(self, G, verbose=False):
    self.G = G
    self.verbose = verbose
    self.action = {}
    self.goto = {}
    self._build_parsing_table()
    
  def _build_parsing_table(self):
    raise NotImplementedError()

  def __call__(self, w):
    stack = [ 0 ]
    cursor = 0
    output = []
        
    while True:
      state = stack[-1]
      lookahead = w[cursor]

      if self.verbose: 
        print(stack, '<---||--->', w[cursor:])
                
      action, tag = self.action[state, lookahead]      
      match action:
        case self.SHIFT:
          stack.append(lookahead)
          stack.append(tag)
          cursor += 1
        case self.REDUCE:
          production = self.G.Productions[tag]
          X, beta = production
          for i in range(2 * len(beta)):
            stack.pop()
          l = stack[-1]
          stack.append(X.Name)
          stack.append(self.goto[l,X])
          output.append(production)
        case self.OK:
          break
        case _:
          raise Exception
        
    return output

class LR1Parser(ShiftReduceParser):
  def _build_parsing_table(self):
    G = self.G.AugmentedGrammar(True)
        
    automaton = build_LR1_automaton(G)
    for i, node in enumerate(automaton):
      if self.verbose: 
        print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
      node.idx = i

    for node in automaton:
      idx = node.idx
      for item in node.state:
        # Fill `self.Action` and `self.Goto` according to `item`
        X = item.production.Left
        symbol = item.NextSymbol
        if X == G.startSymbol and item.IsReduceItem:
          self._register(self.action,(idx,G.EOF),(self.OK,0))
        elif item.IsReduceItem:
          k = self.G.Productions.index(item.production)
          for s in item.lookaheads:                        
            self._register(self.action,(idx,s),(self.REDUCE,k))
        elif symbol.IsTerminal:
          self._register(self.action,(idx,symbol),(self.SHIFT,node.transitions[symbol.Name][0].idx))
        else:
          self._register(self.goto,(idx,symbol),node.transitions[symbol.Name][0].idx)
        
  @staticmethod
  def _register(table, key, value):
    assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
    table[key] = value