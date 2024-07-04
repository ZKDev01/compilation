from tools.cmp.pycompiler import *
from tools.cmp.automata import State, lr0_formatter, multiline_formatter
from tools.cmp.utils import ContainerSet

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

def compute_firsts(G: Grammar):
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

def compute_follows(G: Grammar, firsts):
  follows = { }
  change = True

  local_firsts = {}
  
  for nonterminal in G.nonTerminals:
    follows[nonterminal] = ContainerSet()
  follows[G.startSymbol] = ContainerSet(G.EOF)
  
  while change:
    change = False
    
    for production in G.Productions:
      X = production.Left
      alpha = production.Right
      follow_X = follows[X]
      
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

  return follows

def build_LR0_automaton(G: Grammar):
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

def build_LR1_automaton(G: Grammar) -> State:
  assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
  firsts = compute_firsts(G)
  firsts[G.EOF] = ContainerSet(G.EOF)
    
  start_production = G.startSymbol.productions[0]
  start_item = Item(start_production, 0, lookaheads=(G.EOF,))
  start = frozenset([start_item])
    
  closure = LR1Parser.closure_lr1(start, firsts)
  automaton = State(frozenset(closure), True)
    
  pending = [ start ]
  visited = { start: automaton }
    
  while pending:
    current = pending.pop()
    current_state = visited[current]
        
    for symbol in G.terminals + G.nonTerminals:
      next_items = LR1Parser.goto_lr1(current_state.state, symbol, just_kernel=True)
      if not next_items:
        continue
      try:
        next_state = visited[next_items]
      except KeyError:                    
        closure = LR1Parser.closure_lr1(next_items, firsts)
        next_state = visited[next_items] = State(frozenset(closure), True)
        pending.append(next_items)                               
            
      current_state.add_transition(symbol.Name, next_state)
    
  automaton.set_formatter(multiline_formatter)
  return automaton

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
                    raise Exception('La gramatica no es LL(1)')
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
           

def evaluate_reverse_parse(right_parse, operations, tokens):
  if not right_parse or not operations or not tokens:
    return

  right_parse = iter(right_parse)
  tokens = iter(tokens)
  stack = []
  for operation in operations:
    if operation == ShiftReduceParser.SHIFT:
      token = next(tokens)
      stack.append(token.lex)
    elif operation == ShiftReduceParser.REDUCE:
      production = next(right_parse)
      head, body = production
      attributes = production.attributes
      assert all(rule is None for rule in attributes[1:]), 'There must be only synteticed attributes.'
      rule = attributes[0]
      if len(body):
        synteticed = [None] + stack[-len(body):]
        value = rule(None, synteticed)
        stack[-len(body):] = [value]
      else:
        stack.append(rule(None, None))
    else:
      raise Exception('Invalid action!!!')

  assert len(stack) == 1
  assert isinstance(next(tokens).token_type, EOF)
  return stack[0]

def closure_lr1(items, firsts):
  closure = ContainerSet(*items)
    
  changed = True
  while changed:
    changed = False
        
    new_items = ContainerSet()
    for item in closure:
      new_items.extend(LR1Parser.expand(item, firsts))        

    changed = closure.update(new_items)
        
  return compress(closure)

def expand(item: Item, firsts: dict[Symbol: ContainerSet]) -> list[Item]:
  next_symbol = item.NextSymbol
  if next_symbol is None or not next_symbol.IsNonTerminal:
    return []
  
  lookaheads = ContainerSet()
  for preview in item.Preview():
    lookaheads.hard_update(compute_local_first(firsts, preview))

  assert not lookaheads.contains_epsilon

  child_items = []
  for production in next_symbol.productions:
    child_items.append(Item(production, 0, lookaheads))
  return child_items

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

def goto_lr1(items, symbol: Symbol, firsts: dict[Sentence:ContainerSet] = None, just_kernel: bool = False):
  assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
  items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
  return items if just_kernel else LR1Parser.closure_lr1(items, firsts)


class ShiftReduceParser:
  SHIFT = 'SHIFT'
  REDUCE = 'REDUCE'
  OK = 'OK'
    
  def __init__(self, G: Grammar, verbose=False):
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

class LR1Parser(ShiftReduceParser):
  def _build_parsing_table(self):
    G = self.G.AugmentedGrammar(True)
        
    automaton = self.build_LR1_automaton(G)
    for i, node in enumerate(automaton):
      if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
      node.idx = i

    for node in automaton:
      idx = node.idx
      for item in node.state:                
        if item.IsReduceItem:
          production = item.production
          if production.Left == G.startSymbol:
            self._register(self.action,(idx,G.EOF),(self.OK,None))
          else:
            for symbol in item.lookaheads:
              self._register(self.action,(idx,symbol),(self.REDUCE,production))
        else:
          symbol = item.NextSymbol
          goto_node = node[symbol.Name][0]
          if symbol.IsTerminal:
            self._register(self.action,(idx,symbol),(self.SHIFT,goto_node.idx))
          else:
            self._register(self.goto,(idx,symbol),goto_node.idx)
      
  @staticmethod
  def _register(table: dict, key: tuple[int,Symbol], value):
    assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!'
    table[key] = value

