from cmp.pycompiler import Grammar
from cmp.utils import Token
from cmp.ast import *
from evaluate import evaluate_parse

from parsers import LR1Parser, LL1Parser, evaluate_reverse_parse
from automata import NFA, nfa_to_dfa, automata_minimization, automata_concatenation, automata_closure, automata_union

class EpsilonNode(AtomicNode):
  def evaluate(self):
    return NFA(states=1, finals=[0], transitions={})
    
class SymbolNode(AtomicNode):
  def evaluate(self):
    s = self.lex
    return NFA(states=2, finals=[1], transitions={(0, s): [1]})    
    
class UnionNode(BinaryNode):
  @staticmethod
  def operate(lvalue, rvalue):        
    return automata_union(lvalue,rvalue)

class ConcatNode(BinaryNode):
  @staticmethod
  def operate(lvalue, rvalue):        
    return automata_concatenation(lvalue,rvalue)
    
class ClosureNode(UnaryNode):
  @staticmethod
  def operate(value: NFA):        
    return automata_closure(value)

class PositiveClosureNode(UnaryNode):
  @staticmethod
  def operate(value: NFA):        
    return automata_concatenation(value, automata_closure(value))
    
class ZeroOrOneNode(UnaryNode):
  @staticmethod
  def operate(value: NFA):        
    return automata_union(value,EpsilonNode(G.EOF).evaluate())
    
class CharClassNode(Node):
  def __init__(self, symbols: list[SymbolNode]) -> None:
    self.symbols = symbols
  def evaluate(self):
    value = self.symbols[0].evaluate()  
    for symbol in self.symbols[1:]:            
      value = automata_union(value, symbol.evaluate())  
    return value

class RangeNode(Node):
  def __init__(self, first: SymbolNode, last: SymbolNode) -> None:
    self.first = first
    self.last = last
  def evaluate(self):
    value = [self.first]
    for i in range(ord(self.first.lex)+1,ord(self.last.lex)):
      value.append(SymbolNode(chr(i)))
    value.append(self.last)
    return CharClassNode(value).evaluate()  

G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, S = G.NonTerminals('T F A S')
pipe, star, plus, minus, quest, opar, cpar, obrack, cbrack, symbol, epsilon = G.Terminals('| * + - ? ( ) [ ] symbol ε')
scape = G.Terminal("\\")

E %= T, lambda h,s: s[1]
E %= E + pipe + T, lambda h,s: UnionNode(s[1],s[3])

T %= F, lambda h,s: s[1]
T %= T + F, lambda h,s: ConcatNode(s[1],s[2])

F %= A, lambda h,s: s[1]
F %= A + star, lambda h,s: ClosureNode(s[1])
F %= A + plus, lambda h,s: PositiveClosureNode(s[1])
F %= A + quest, lambda h,s: ZeroOrOneNode(s[1])

A %= symbol, lambda h,s: SymbolNode(s[1])
A %= scape + symbol, lambda h,s: SymbolNode(s[2])
A %= epsilon, lambda h,s: EpsilonNode(s[1])                                                
A %= opar + E + cpar, lambda h,s: s[2]
A %= obrack + S + cbrack, lambda h,s: CharClassNode(s[2])

S %= symbol, lambda h,s: [SymbolNode(s[1])]
S %= scape + symbol, lambda h,s: [SymbolNode(s[2])]
S %= symbol + S, lambda h,s: [SymbolNode(s[1])] + s[2]
S %= symbol + minus + symbol, lambda h,s: RangeNode(SymbolNode(s[1]),SymbolNode(s[3]))
S %= symbol + minus + symbol + S, lambda h,s: RangeNode(SymbolNode(s[1]),SymbolNode(s[3])) + s[4]

class Regex:
  def __init__(self, text: str) -> None:
    self.text = text 
    self.automaton = ''

  def regex_tokenizer(self, G, skip_whitespaces=True) -> list[Token]:
    tokens = []
    fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        'ε': Token('ε', epsilon),
        '(': Token('(', opar),
        ')': Token(')', cpar),
        '\\': Token('\\',scape)
    }

    for char in self.text:
        if skip_whitespaces and char.isspace():
            continue
        if len(tokens)>0 and tokens[-1].lex == '\\':
                tokens.append(Token(char, symbol))
        else:
            try:
                tokens.append(fixed_tokens[char])
            except KeyError:
                tokens.append(Token(char, symbol))

    tokens.append(Token('$', G.EOF))
    return tokens
  
  def build_automaton(self):
    tokens = self.regex_tokenizer(G)
    left_parser = LL1Parser(G)
    parse = left_parser(tokens)
    ast = evaluate_parse(parse, tokens)
    nfa = ast.evaluate()
    dfa = nfa_to_dfa(automaton=nfa)
    return automata_minimization(automaton=dfa)

# Test the Regex class
regex = Regex("a(b|c)*d")
automaton = regex.build_automaton()
automaton