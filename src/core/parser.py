from tools.cmp.evaluation import evaluate_reverse_parse
from tools.cmp.utils import Token
from tools.parsers import LR1Parser
from core.grammar import G

def parse(tokens: list[Token]):
  parse = __build_parser()
  # parse(w=List[Token], shift-reduce=True)
  # recibir el ast y aplicar evaluate_reverse_parse
  # return ast

def __build_parser() -> LR1Parser:
  return LR1Parser(G=G, verbose=False)