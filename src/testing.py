from tools.automata import NFA, DFA, automata_union, automata_concatenation, automata_closure, nfa_to_dfa, state_minimization, distinguish_states, automata_minimization

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
  automaton_nfa_3 = NFA(states=3, finals=[2], transitions={
    (0,'a'): [ 0 ], 
    (0,'b'): [ 0, 1 ],
    (1,'a'): [ 2 ],
    (1,'b'): [ 2 ],
  })
  automaton_nfa_4 = NFA(states=5, finals=[4], transitions={
    (0,'a'): [ 0, 1 ],
    (0,'b'): [ 0, 2 ],
    (0,'c'): [ 0, 3 ],
    (1,'a'): [ 1, 4 ],
    (1,'b'): [ 1 ],
    (1,'c'): [ 1 ],
    (2,'a'): [ 2 ],
    (2,'b'): [ 2, 4 ],
    (2,'c'): [ 2 ],
    (3,'a'): [ 3 ],
    (3,'b'): [ 3 ],
    (3,'c'): [ 3, 4 ],
  })

  automaton_dfa_1 = DFA(states=3, finals=[2], transitions={
    (0, 'a'): 0,
    (0, 'b'): 1,
    (1, 'a'): 2,
    (1, 'b'): 1,
    (2, 'a'): 0,
    (2, 'b'): 1,
  })
  automaton_dfa_2 = DFA(states=2, finals=[1], transitions={
    (0,'a'):0,
    (0,'b'):1,
    (1,'a'):0,
    (1,'b'):1,
  })
  automaton_dfa_3 = DFA(states=5, finals=[4], transitions={
    (0,'a'): 1,
    (0,'b'): 2,
    (1,'a'): 1,
    (1,'b'): 3,
    (2,'a'): 1,
    (2,'b'): 2,
    (3,'a'): 1,
    (3,'b'): 4,
    (4,'a'): 1,
    (4,'b'): 2,
  })

  # DEF TEST
  def test_recognize(automaton: NFA, valid_list: list[str], notvalid_list: list[str]):
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

  def test_union(a1: NFA, a2: NFA, valid_list: list[str], notvalid_list: list[str]):
    automaton = automata_union(a1=a1, a2=a2)
    test_recognize(automaton=automaton, valid_list=valid_list, notvalid_list=notvalid_list)

  def test_concatenation(a1: NFA, a2: NFA, valid_list: list[str], notvalid_list: list[str]):
    automaton = automata_concatenation(a1=a1, a2=a2)
    test_recognize(automaton=automaton, valid_list=valid_list, notvalid_list=notvalid_list)

  def test_closure(automaton: NFA, valid_list: list[str], notvalid_list: list[str]):
    automaton = automata_closure(a1=automaton) 
    test_recognize(automaton=automaton, valid_list=valid_list, notvalid_list=notvalid_list)

  def test_state_minimization(automaton: NFA, len_states: int):
    states = state_minimization(automaton=automaton)
    for members in states.groups:
      all_in_finals = all([m.value in automaton.finals for m in members])
      none_in_finals = all([m.value not in automaton.finals for m in members])
      assert all_in_finals or none_in_finals
    assert len(states) == 4

  def test_minimization(automaton: NFA, states: int, valid_list: list[str], notvalid_list: list[str]):
    automaton = automata_minimization(automaton=automaton)
    assert automaton.states == states
    test_recognize(automaton=automaton, valid_list=valid_list, notvalid_list=notvalid_list)

  # CASE TEST
  test_recognize(automaton=automaton_dfa_1, 
    valid_list=['ba','aababbaba'], 
    notvalid_list=['', 'aabaa', 'aababb'])
  test_recognize(automaton=automaton_nfa_2,
    valid_list=['','a','b','cccccc','adddd','bdddd'],
    notvalid_list=['dddddd','cdddd','aa','ab','ddddc'])
  test_recognize(automaton=automaton_nfa_4,
    valid_list=['abccac','bbbbbbbbaa','cac'],
    notvalid_list=['abbbbc','a','','acacacaccab'])
  test_move(automaton=automaton_nfa_2, 
    states=[[1], [2], [1,5]], 
    symbols=['a','a','d'],
    results=[ set(), {4}, {5} ])
  test_move(automaton=automaton_nfa_3,
    states=[[0,1], [0,1]],
    symbols=['a','b'],
    results=[ {0, 2}, {0, 1, 2} ] )
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
  test_nfa_to_dfa(automaton=automaton_nfa_3,
    valid_list=['aba','bb','aaaaaaaaaaaba'],
    notvalid_list=['aaa','ab','b',''])
  test_nfa_to_dfa(automaton=automaton_nfa_4,
    valid_list=['abccac','bbbbbbbbaa','cac'],
    notvalid_list=['abbbbc','a','','acacacaccab'])
  test_union(a1=automaton_dfa_2, a2=automaton_dfa_2, 
    valid_list=['b','abbb','abaaababab'],
    notvalid_list=['','a','abbbbaa'])
  test_concatenation(a1=automaton_dfa_2, a2=automaton_dfa_2, 
    valid_list=['bb','abbb','abaaababab'],
    notvalid_list=['','a','b','ab','aaaab','abbbbaa'])
  test_closure(automaton=automaton_dfa_2,
    valid_list=['','b','ab','bb','abbb','abaaababab'],
    notvalid_list=['a','abbbbaa'])
  test_state_minimization(automaton=automaton_dfa_3, len_states=4)
  test_minimization(automaton=automaton_dfa_3, 
    states=4,
    valid_list=['ababbaabb','abb'],
    notvalid_list=['','ab','aaaaa','bbbbb','abbabababa'])


def main() -> None:
  testing_automata()

  print("ALL TEST - OK!")

if __name__ == '__main__':
  main()
