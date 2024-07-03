from cmp.pycompiler import EOF

def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return
    
    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)
    
    assert isinstance(next(tokens).token_type, EOF)
    return result
    

def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes
    
    synteticed = [None] * (len(body) + 1) 
    inherited = [None] * (len(body) + 1)
    inherited[0] = inherited_value # value inherited by the head
    
    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            synteticed[i] = next(tokens).lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            
            lambda_inherit = attributes[i] # func that compute inherited value to the next prod
            if lambda_inherit is not None:
                inherited[i] = lambda_inherit(inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])
    
    lambda_synt = attributes[0] # func that compute the synteticed value of the head
    if lambda_synt is None:
        return None
    else:
        return lambda_synt(inherited, synteticed)