from tools.automata import NFA, DFA, automata_union, nfa_to_dfa

def testing_automata():
  
  # DEF AUTOMATON
  automaton_nfa_1 = NFA(states=3, finals=[2], transitions={
    (0, 'a'): [0],
    (0, 'b'): [0, 1],
    (1, 'a'): [2]
  })
  automaton_nfa_2 = NFA(states=6, finals=[3, 5], transitions={
    (0, ''): [ 1, 2 ],
    (1, ''): [ 3 ],
    (1,'b'): [ 4 ],
    (2,'a'): [ 4 ],
    (3,'c'): [ 3 ],
    (4, ''): [ 5 ],
    (5,'d'): [ 5 ]
  })

  automaton_dfa_1 = DFA(states=3, finals=[2], transitions={
    (0, 'a'): 0,
    (0, 'b'): 1,
    (1, 'a'): 2,
    (1, 'b'): 1,
    (2, 'a'): 0,
    (2, 'b'): 1,
  })

  # DEF TEST
  def test_recognize(automaton: DFA, valid_list: list[str], notvalid_list: list[str]):
    valid_results: list[bool] = [automaton.recognize(string=string) for string in valid_list]
    notvalid_results: list[bool] = [not automaton.recognize(string=string) for string in notvalid_list]
    assert all(valid_results)
    assert all(notvalid_results)

  def test_move(automaton: NFA, states: list[list[int]], symbols: list[str], results: list[set]):
    for i in range(0, len(states)):
      assert automaton._move(states=states[i], symbol=symbols[i]) == results[i]

  def test_epsilon_closure(automaton: NFA, states: list[list[int]], results: list[set]):
    for i in range(0, len(states)):
      assert automaton.epsilon_closure(states=states[i]) == results[i]

  def test_nfa_to_dfa(automaton: NFA, valid_list: list[str], notvalid_list: list[str]):
    automaton = nfa_to_dfa(automaton=automaton)
    test_recognize(automaton=automaton, valid_list=valid_list, notvalid_list=notvalid_list)

  # CASE TEST
  test_recognize(automaton=automaton_dfa_1, 
    valid_list=['ba','aababbaba'], 
    notvalid_list=['', 'aabaa', 'aababb'])
  test_move(automaton=automaton_nfa_2, 
    states=[[1], [2], [1,5]], 
    symbols=['a','a','d'],
    results=[ set(), {4}, {5} ])
  test_epsilon_closure(automaton=automaton_nfa_2, 
    states=[
      [0],
      [0,4],
      [1,2,4]
    ], 
    results=[
      {0,1,2,3},
      {0,1,2,3,4,5},
      {1,2,3,4,5}
    ])
  test_nfa_to_dfa(automaton=automaton_nfa_2,
    valid_list=['','a','b','cccccc','addd','bdddd'], 
    notvalid_list=['dddddd', 'cdddd', 'aa','ab','ddddc'])

  print("OK")


def main() -> None:
  testing_automata()

if __name__ == '__main__':
  main()
