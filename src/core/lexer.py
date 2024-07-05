from core.grammar import *

from tools.cmp.utils import Token
from tools.cmp.automata import State
from tools.regex import Regex

class Lexer:
  def __init__(self, table, eof):
    self.eof = eof
    self.regexs = self._build_regexs(table)
    self.automaton = self._build_automaton()
    
  def _build_regexs(self, table):
    regexs = []
    for n, (token_type, regex) in enumerate(table):
      automaton = Regex(regex).automaton
      automaton = State.from_nfa(automaton)
      for state in automaton:
        if state.final:
          state.tag = (token_type,n)
      regexs.append(automaton)
    return regexs
    
  def _build_automaton(self):
    start = State('start')
    for automaton in self.regexs:
      start.add_epsilon_transition(automaton) 
    return start.to_deterministic()    
        
  def _walk(self, string):
    state = self.automaton
    final = state if state.final else None
    final_lex = lex = ''
        
    for symbol in string:       
      try:
        state = state[symbol][0] 
        lex = lex + symbol
      except TypeError:
        break  

    final = state                    
    final.tag = (None, float('inf'))
    for state in final.state:
      if state.final and state.tag[1] < final.tag[1]:
        final.tag = state.tag
    final_lex = lex

    return final, final_lex
    
  def _tokenize(self, text: str):
    remaining_text = text
    while True:
      final_state, final_lex = self._walk(remaining_text)

      if final_lex == '':
        yield text.rsplit(remaining_text)[0], final_state.tag[0]
        return
            
      yield final_lex, final_state.tag[0] 
      remaining_text = remaining_text.replace(final_lex,'',1)
      if remaining_text == '':
        break
        
    yield '$', self.eof
    
  def __call__(self, text):
    return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]

def generate_lexer():
  table = [ ]

  table.append( ('space', SPACE) )
  table.append( (string_, STRINGS_VALUES))
  table.append( (number,  INTEGER))

  table.append( (id, IDENTIFIER))

  table.append( (multiplication,r'\*'))
  table.append( (plus,'+'))
  table.append( (ocbracket,r'\('))
  table.append( (ccbracket,r'\)'))
  table.append( (semicolon,';'))
  table.append( (minus,'-'))
  table.append( (division,'/'))
  table.append( (obracket,'{'))
  table.append( (cbracket,'}'))
  table.append( (logical_and,'&'))
  table.append( (logical_or,r'\|'))
  table.append( (logical_not,'!'))
  table.append( (comparator_greater,'>'))
  table.append( (comparator_less,'<'))
  table.append( (comparator_less_equal,'<='))
  table.append( (comparator_greater_equal,'>='))
  table.append( (comparator_equal,'=='))
  table.append( (comparator_notequal,'!='))
  table.append( (exponential,'^'))
  table.append( (osbracket,'['))
  table.append( (csbracket,']'))
  table.append( (gen_pattern_symbol,r'\|\|'))
  table.append( (string_operator_space,'@@'))
  table.append( (string_operator,'@'))
  table.append( (assignation,':='))
  table.append( (inicialization,'='))
  table.append( (comma,','))
  table.append( (module,'%'))
  table.append( (function_arrow,'=>'))
  table.append( (type_assignation,':'))
  table.append( (dot_,'.'))
  table.append( (while_,'while'))
  table.append( (protocol,'protocol'))
  table.append( (extends,'extends'))
  table.append( (for_,'for'))
  table.append( (let,'let'))
  table.append( (in_,'in'))
  table.append( (function,'function'))
  table.append( (if_,'if'))
  table.append( (elif_,'elif'))
  table.append( (else_,'else'))
  table.append( (boolean_true,'true'))
  table.append( (boolean_false,'false'))
  table.append( (new_,'new'))
  table.append( (type_,'type'))
  table.append( (inherits,'inherits'))
  
  return Lexer(table=table, eof=G.EOF)

def tokenizer(code: str, lexer: Lexer):
  try:
    tokens = lexer(code)
    return tokens
  except Exception:
    print("Error al tokenizar")
    return
