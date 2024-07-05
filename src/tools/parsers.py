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





class LL1Parser():
  def __init__(self, G):
    self.G = G
    self.M: dict[(NonTerminal, Terminal), Production] = {}
    self.firsts = compute_firsts(self.G)
    self.follows = compute_follows(self.G, self.firsts)
    self._build_parsing_table()

  def _build_parsing_table(self):
    G = self.G
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
    M = {} # [NonTerminal, Terminal] -> [Production]
    
    for production in G.Productions:
      X = production.Left
      alpha = production.Right
        
      if not alpha.IsEpsilon:
        for first in firsts[alpha]:
          if (X, first) in M:
            raise Exception(f'The grammar is not LL(1) because the pair({X}, {first}) has already asociated the production {M[X, first]} and want assign the production {production}')
          M[X, first] = [production, ]
      else:
        for follow in follows[X]:
          if (X, follow) in M:
            raise Exception('The grammar is not LL(1)')
          M[X, follow] = [production, ]
    self.M = M

  def __call__(self, w: list[Symbol]):
    G, M = self.G, self.M

    stack =  [G.EOF, G.startSymbol]
    cursor = 0
    output = []
    
    while True:
      top = stack.pop()
      a = w[cursor]
      
      if top.IsEpsilon:
        pass
      elif top.IsTerminal:
        assert top == a
        if top == G.EOF:
          break
        cursor += 1
      else:
        [production, ] = M[top,a]
        output.append(production)
        production = list(production.Right)
        stack.extend(production[::-1])

    return output




class ShiftReduceParser:
  SHIFT = 'SHIFT'
  REDUCE = 'REDUCE'
  OK = 'OK'
    
  def __init__(self, G, verbose=False):
    self.verbose = verbose
    self.action = {}
    self.goto = {}
    self.G = G
    self._build_parsing_table()
    
  def _build_parsing_table(self):
    raise NotImplementedError()

  def __call__(self, w: list[Token], get_shift_reduce=False):
    stack = [ 0 ]
    cursor = 0
    output = []
    operations = []
        
    while True:
      state = stack[-1]
      lookahead = w[cursor].token_type
      if self.verbose: 
        print(stack, '<---||--->', w[cursor:])
      # DETECT ERROR
      if (state, lookahead) not in self.action:
        print('pila',stack)
        print((state, lookahead))
        print((w[:cursor], lookahead))
        print('Error, Aborting...')
        return None
      action, tag = self.action[state, lookahead]
      # CASE: SHIFT
      if action == self.SHIFT:
        operations.append(self.SHIFT)
        stack += [lookahead, tag] # symbol, id
        cursor += 1
      # CASE: REDUCE
      elif action == self.REDUCE:
        operations.append(self.REDUCE)
        output.append(tag) # tag is a production
        head, body = tag
        for symbol in reversed(body):
          stack.pop()
          pop=stack.pop() # remove tag(id)
          assert pop == symbol # remove symbol(lookahead)
        # transition with symbol(head)
        state=stack[-1]
        goto=self.goto[state,head]
        stack+=[head,goto]
      # CASE: OK
      elif action == self.OK:
        stack.pop()
        pop = stack.pop()
        assert pop == self.G.startSymbol
        assert len(stack) == 1 # initial number 0
        return output if not get_shift_reduce else (output, operations)
      else:
      # INVALID CASE
        raise Exception(f'{action} is an invalid action!!')




def build_LR0_automaton(G: Grammar) -> State:
  assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

  start_production = G.startSymbol.productions[0]
  start_item = Item(start_production, 0)
  automaton = State(start_item, True)

  pending = [ start_item ]
  visited = { start_item: automaton }

        
  while pending:
    current_item = pending.pop()
    if current_item.IsReduceItem:
      continue
        
    next_symbol = current_item.NextSymbol
    next_item = current_item.NextItem()        
    if not next_item in visited:
      visited[next_item] = State(next_item,True)
      pending.append(next_item)

    epsilon_transitions_states = []
    if next_symbol.IsNonTerminal:            
      for production in G.Productions:
        if production.Left == next_symbol:
          item = Item(production,0)                    
          if not item in visited:
            visited[item] = State(item,True)
            pending.append(item)
          epsilon_transitions_states.append(visited[item])

    current_state = visited[current_item]
    current_state.add_transition(next_symbol.Name,visited[next_item])             
    for state in epsilon_transitions_states:
          current_state.add_epsilon_transition(state)

  return automaton

class SLR1Parser(ShiftReduceParser):
  def _build_parsing_table(self):
    G = self.G.AugmentedGrammar(True)
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
        
    automaton = build_LR0_automaton(G).to_deterministic()
    for i, node in enumerate(automaton):
      if self.verbose: 
        print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
      node.idx = i

    for node in automaton:
      idx = node.idx
      for state in node.state:
        item = state.state
        # Fill `self.Action` and `self.Goto` according to `item`
        X = item.production.Left
        symbol = item.NextSymbol
        if X == G.startSymbol and item.IsReduceItem:
          self._register(self.action,(idx,G.EOF),(self.OK,0))
        elif item.IsReduceItem:
          k = self.G.Productions.index(item.production)
          for c in follows[X]:                        
            self._register(self.action,(idx,c),(self.REDUCE,k))
        elif symbol.IsTerminal:
          self._register(self.action,(idx,symbol),(self.SHIFT,node.transitions[symbol.Name][0].idx))
        else:
          self._register(self.goto,(idx,symbol),node.transitions[symbol.Name][0].idx)

  @staticmethod
  def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value