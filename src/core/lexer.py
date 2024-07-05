from core.grammar import *

from tools.cmp.utils import Token
from tools.cmp.automata import State
from tools.regex import Regex

import string

class Lexer:

  def __init__(self, table, eof):
    self.eof = eof
    self.regexs = self._build_regexs(table)
    self.automaton = self._build_automaton()

  def _build_regexs(self, table):
    regexs = []
    for n, (token_type, regex) in enumerate(table):
      regx = Regex(regex)
      automaton = State.from_nfa(regx.automaton)
      for state in automaton:
        if state.final:
          state.tag = (n, token_type)
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
        lex += symbol
        if state.final:
          final = state if state.final else final
          final_lex = lex
      except TypeError:
        break
    return final, final_lex
  
  def _tokenize(self, text):
    remaining_text = text
    while remaining_text:
      final_state, lexeme = self._walk(remaining_text)
      if lexeme == '':
        raise KeyError('Unexcepted character: ', remaining_text[0])
      if final_state:
        sorted_states = [s for s in final_state.state if s.tag is not None]
        sorted_states.sort(key= lambda x: x.tag[0])
        yield lexeme, sorted_states[0].tag[1] 
        remaining_text = remaining_text[len(lexeme):]
      else:
        yield remaining_text[0], 'ERROR'
        remaining_text = remaining_text[1:]
    yield '$', self.eof
  
  def __call__(self, text: str):
    return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]


digits = '|'.join(str(i) for i in range(0, 10))
nonzerodigits = '|'.join(str(i) for i  in range(1, 10))
lowers = '|'.join(chr(i) for i in range(ord('a'), ord('z') + 1))
uppers = '|'.join(chr(i) for i in range(ord('A'), ord('Z') + 1))

def mapping(string):
  if string == '|':
    return r'\|'
  if string == '*':
    return r'\*'
  if string == '(':
    return r'\('
  if string == ')':
    return r'\)'           
  else:
    return string

printables = '|'.join([printable for printable in list(map(mapping,string.printable))])
STRINGS_VALUES = f'(\")({printables})*(\")'
INTEGER = f'({digits})(.|{EPSILON})({digits})*'
SPACE = '(\n|\t|\f|\r|\v| )(\n|\t|\f|\r|\v| )*'

id = f'({uppers}|{lowers}|_)({uppers}|{lowers}|{digits}|_)*'

def build_lexer():
  table = []

  table.append(('space',SPACE))
  table.append((number, INTEGER))

  table.append((mult,r'\*'))
  table.append((plus_,'+'))
  table.append((open_par,r'\('))
  table.append((closed_par,r'\)'))
  table.append((semicolon,';'))
  table.append((minus_,'-'))
  table.append((div,'/'))
  table.append((open_bracket,'{'))
  table.append((closed_bracket,'}'))
  table.append((and_,'&'))
  table.append((or_,r'\|'))
  table.append((not_,'!'))
  table.append((gt,'>'))
  table.append((lt,'<'))
  table.append((lte,'<='))
  table.append((gte,'>='))
  table.append((eq,'=='))
  table.append((neq,'!='))
  table.append((exponentiation,'^'))
  table.append((open_square_braket,'['))
  table.append((close_square_braket,']'))
  table.append((gen_pattern_symbol,r'\|\|'))
  table.append((string_oper_space,'@@'))
  table.append((string_oper,'@'))
  table.append((assign,':='))
  table.append((init,'='))
  table.append((comma,','))
  table.append((module_oper,'%'))
  table.append((func_arrow,'=>'))
  table.append((type_asignator,':'))
  table.append((dot,'.'))
  table.append((while_,'while'))
  table.append((protocol,'protocol'))
  table.append((extends,'extends'))
  table.append((for_,'for'))
  table.append((let,'let'))
  table.append((in_,'in'))
  table.append((func,'function'))
  table.append((if_,'if'))
  table.append((elif_,'elif'))
  table.append((else_,'else'))
  table.append((true,'true'))
  table.append((false,'false'))
  table.append((new,'new'))
  table.append((type,'type'))
  table.append((inherits,'inherits'))
  table.append((string_,STRINGS_VALUES))
  table.append((ID,id))

  return Lexer(table,G.EOF)


def cleaner(tokens: list[Token]):
  i = 0
  while i < len(tokens):
    if tokens[i].token_type == 'space':
      tokens.remove(tokens[i])
    else:
      i += 1

def tokenizer(code: str, lexer: Lexer = None):
  if lexer is None:
    lexer = build_lexer()
  try:
    tokens = lexer(code)
    cleaner(tokens)
    return tokens
  except Exception as e:
    print(e)