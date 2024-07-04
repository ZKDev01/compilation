from tools.cmp.evaluation import evaluate_reverse_parse
from tools.cmp.pycompiler import Grammar
from tools.cmp.utils import Token
from tools.parsers import LR1Parser
from core.grammar import G

class Parser:
  def __init__(self, G: Grammar) -> None:
    self.parse = LR1Parser(G=G, verbose=False)

  def parse(tokens: list[Token]):
    pass
    # parse(w=List[Token], shift-reduce=True)
    # recibir el ast y aplicar evaluate_reverse_parse
    # return ast

