from tools.cmp.utils import ContainerSet, DisjointSet

class NFA:
  def __init__(self, 
      states: int, 
      finals: list[int], 
      transitions: dict[ (int,str), list[int] ], 
      start: int = 0):
    self.states = states
    self.finals = set(finals)
    self.map = transitions
    self.start = start

    self.vocabulary = set()
    self.transitions = { state: {} for state in range(states) }
    
    for (origin, symbol), destinations in transitions.items():
      assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
      self.transitions[origin][symbol] = destinations
      self.vocabulary.add(symbol)
    self.vocabulary.discard('')

  def epsilon_transitions(self, state):
    assert state in self.transitions, 'Invalid state'
    try:
      return self.transitions[state]['']
    except KeyError:
      return ()

  def _move(self, states: list[int], symbol: str):
    moves = set()
    for state in states:
      try:
        moves.update(self.map[(state,symbol)])
      except:
        pass
    return moves

  def epsilon_closure(self, states: list):
    pending = [ s for s in states ]
    closure = { s for s in states }
    
    while pending:
      state = pending.pop()
      try:
        new_states = self.map[(state,'')]
        closure.update(new_states)
        closure.update(self.epsilon_closure(new_states).set)
      except KeyError:
        pass     
    
    return ContainerSet(*closure)





class DFA(NFA):
  def __init__(self, states, finals, transitions, start=0):
    assert all(isinstance(value, int) for value in transitions.values())
    assert all(len(symbol) > 0 for origin, symbol in transitions)
        
    transitions = { key: [value] for key, value in transitions.items() }
    NFA.__init__(self, states, finals, transitions, start)
    self.current = start
        
  def _move(self, symbol):
    try:
      self.current = self.transitions[self.current][symbol][0]
      return True
    except KeyError:
      self.current = None
      return False
    
  def _reset(self):
    self.current = self.start
        
  def recognize(self, string: str):
    self._reset()
    for symbol in string:
      if not self._move(symbol):
        return False
    return self.current in self.finals



def nfa_to_dfa(automaton: NFA):
    
  transitions = {}
    
  start = automaton.epsilon_closure([automaton.start])
  start.id = 0
  start.is_final = any(s in automaton.finals for s in start)
  states = [ start ]
  state_sets = [ start.set ]

  pending = [ start ]
  index = 0
  while pending:
    state = pending.pop()
        
    for symbol in automaton.vocabulary:
      next_state_set = automaton.epsilon_closure(automaton._move(list(state.set), symbol)).set

      if not next_state_set: 
        continue              

      try:
        i = state_sets.index(next_state_set)
        next_state = states[i]
      except ValueError:                
        next_state = ContainerSet(*next_state_set)
        index += 1
        next_state.id = index
        next_state.is_final = any(s in automaton.finals for s in next_state)

        states.append(next_state)
        state_sets.append(next_state_set)
        pending.append(next_state)          

      try:
        transitions[state.id, symbol]
        assert False, 'Invalid DFA!!!'
      except KeyError:
        transitions[state.id,symbol] = next_state.id
    
  finals = [ state.id for state in states if state.is_final ]
  dfa = DFA(len(states), finals, transitions)
  return dfa



def automata_union(a1: NFA, a2: NFA):
  transitions = {}
    
  start = 0
  d1 = 1
  d2 = a1.states + d1
  final = a2.states + d2
    
  for (origin, symbol), destinations in a1.map.items():
    # Relocate a1 transitions ...
    transitions[d1 + origin, symbol] = [d1 + d for d in destinations]

  for (origin, symbol), destinations in a2.map.items():        
    # Relocate a2 transitions ...
    transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    
  # Add transitions from start state ...
  transitions[start, ''] = [d1,d2]
    
  # Add transitions to final state ...
  transitions[d2 - 1, ''] = [final]
  transitions[final - 1, ''] = [final]
            
  states = a1.states + a2.states + 2
  finals = { final }
    
  return NFA(states, finals, transitions, start)

def automata_concatenation(a1: NFA, a2: NFA):
  pass
