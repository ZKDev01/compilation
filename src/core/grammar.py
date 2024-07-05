import string

from tools.cmp.pycompiler import Grammar
from tools.regex import EPSILON
from tools.ast import * 

G = Grammar()
program = G.NonTerminal('<program>', True)

#region: NON-TERMINALS
inst_list                       = G.NonTerminal('<inst-list>')
param                           = G.NonTerminal('<param>')
program_decl_list               = G.NonTerminal('<program-decl-list>')
program_level_decl              = G.NonTerminal('<program-level-decl>')
inst_wrapper                    = G.NonTerminal('<inst-wrapper>')
inst                            = G.NonTerminal('<inst>')
var_dec                         = G.NonTerminal('<var-dec>')
expression                      = G.NonTerminal('<expression>')
flux_control                    = G.NonTerminal('<flux-control>')
base_exponent                   = G.NonTerminal('<base-exponent>')
scope                           = G.NonTerminal('<scope>')
function_declaration            = G.NonTerminal('<function-decl>')
function_call                   = G.NonTerminal('<function-call>')
type_declaration                = G.NonTerminal('<type-decl>')
id_list                         = G.NonTerminal('<id-list>')
type_instanciation              = G.NonTerminal('<type-instanciation>')
var_asign                       = G.NonTerminal('<var-asign>')
aritmetic_operation             = G.NonTerminal('<aritmetic-operation>')
factor                          = G.NonTerminal('<factor>')
term                            = G.NonTerminal('<term>')
atom                            = G.NonTerminal('<atom>')
var_init                        = G.NonTerminal('<var-init>')
vat_init_list                   = G.NonTerminal('<vat-init-list>')
string_operation                = G.NonTerminal('<string-operation>')
string_atom                     = G.NonTerminal('<string-atom>')
function_full_declaration       = G.NonTerminal('<function-full-decl>')
function_inline_declaration     = G.NonTerminal('<function-inline-decl>')
var_decl_expr                   = G.NonTerminal('<var-decl-expr>')
conditional                     = G.NonTerminal('<conditional>')
inline_conditional              = G.NonTerminal('<inline-conditional>')
full_conditional                = G.NonTerminal('<full-conditional>')
else_statement                  = G.NonTerminal('<else-statement>')
inline_else                     = G.NonTerminal('<inline-else>')
full_else                       = G.NonTerminal('<full-else>')
loop                            = G.NonTerminal('<loop>')
while_loop                      = G.NonTerminal('<while-loop>')
for_loop                        = G.NonTerminal('<for-loop>')
iterable_expression             = G.NonTerminal('<iterable-expression>')
conditional_expresssion         = G.NonTerminal('<conditional-expresssion>')
condition                       = G.NonTerminal('<condition>')
boolean_value                   = G.NonTerminal('<boolean-value>') 
comparation                     = G.NonTerminal('<comparation>')
decl_body                       = G.NonTerminal('<decl-body>')
decl_list                       = G.NonTerminal('<decl-list>')
decl                            = G.NonTerminal('<decl>')
constructor                     = G.NonTerminal('<constructor>')
atribute_declaration            = G.NonTerminal('<atribute-decl>')
method_declaration              = G.NonTerminal('<method-decl>')
function_call                   = G.NonTerminal('<function-call>')
param_list                      = G.NonTerminal('<param-list>')
var_attr                        = G.NonTerminal('<var-attr>')
var_method                      = G.NonTerminal('<var-method>')
identifier                      = G.NonTerminal('<identifier>')
type_anotation                  = G.NonTerminal('<type-anotation>')
protocol_declaration            = G.NonTerminal('<protocol-decl>')
var_use                         = G.NonTerminal('<var-use>')
protocol_body                   = G.NonTerminal('<protocol-body>')
extend_definer                  = G.NonTerminal('<extend-definer>')
virtual_method_list             = G.NonTerminal('<virtual-method-list>')
virtual_method                  = G.NonTerminal('<virtual-method>')
fully_typed_params              = G.NonTerminal('<fully-typed-params>')
fully_typed_param               = G.NonTerminal('<fully-typed-param>')
vector                          = G.NonTerminal('<vector>')
vector_decl                     = G.NonTerminal('<vector-decl>')
generation_pattern              = G.NonTerminal('<generation-pattern>')
func_decl_id                    = G.NonTerminal('<func-decl-id>')
inherits_type                   = G.NonTerminal('<inherits-type>')
#endregion

#region: TERMINALS
semicolon                       = G.Terminal(';')
gen_pattern_symbol              = G.Terminal('||')
while_                          = G.Terminal('while')
for_                            = G.Terminal('for')
obracket                        = G.Terminal('{')
cbracket                        = G.Terminal('}')
let                             = G.Terminal('let')
id                              = G.Terminal('ID')
assignation                     = G.Terminal(':=')
inicialization                  = G.Terminal('=')
in_                             = G.Terminal('in')
inherits                        = G.Terminal('inherits')
comma                           = G.Terminal(',')
number                          = G.Terminal('number')
ocbracket                       = G.Terminal('(')
ccbracket                       = G.Terminal(')')
plus                            = G.Terminal('+')
minus                           = G.Terminal('-')
multiplication                  = G.Terminal('*')
division                        = G.Terminal('/')
module                          = G.Terminal('%')
string_                         = G.Terminal('string')
string_operator                 = G.Terminal('@')
string_operator_space           = G.Terminal('@@')
function                        = G.Terminal('function')
function_arrow                  = G.Terminal('=>')
if_                             = G.Terminal('if')
elif_                           = G.Terminal('elif')
else_                           = G.Terminal('else')
logical_and                     = G.Terminal('&')
logical_or                      = G.Terminal('|')
logical_not                     = G.Terminal('!')
boolean_true                    = G.Terminal('true')
boolean_false                   = G.Terminal('false')
comparator_greater              = G.Terminal('>')
comparator_less                 = G.Terminal('<')
comparator_greater_equal        = G.Terminal('>=')
comparator_less_equal           = G.Terminal('<=')
comparator_equal                = G.Terminal('==')
comparator_notequal             = G.Terminal('!=')
new_                            = G.Terminal('new')
type_                           = G.Terminal('type')
dot_                            = G.Terminal('.')
type_assignation                = G.Terminal(':')
exponential                     = G.Terminal('^')
protocol                        = G.Terminal('protocol')
extends                         = G.Terminal('extends')
osbracket                       = G.Terminal('[')
csbracket                       = G.Terminal(']')
#endregion

#region: PRODUCTIONS
program %= program_decl_list, lambda h,s: ProgramNode(s[1])

program_decl_list %= inst_wrapper, lambda h,s: [s[1]]
program_decl_list %= program_level_decl + program_decl_list, lambda h,s: [s[1]] + s[2]
program_decl_list %= G.Epsilon, lambda h,s: []

program_level_decl %= type_declaration, lambda h,s: s[1]
program_level_decl %= function_declaration, lambda h,s: s[1]
program_level_decl %= protocol_declaration, lambda h,s: s[1]

inst_list %= inst + semicolon, lambda h,s: [s[1]]
inst_list %= inst + semicolon + inst_list, lambda h,s: [s[1]] + s[3]

inst_wrapper %= inst, lambda h,s: s[1]
inst_wrapper %= inst + semicolon, lambda h,s: s[1]

inst %= scope, lambda h,s: s[1]
inst %= flux_control, lambda h,s: s[1]

inst %= expression, lambda h,s: s[1]
inst %= var_dec, lambda h,s: s[1]

var_dec %= let + vat_init_list+ in_ + var_decl_expr, lambda h,s: VarsDeclarationsListNode(s[2], s[4])

var_decl_expr %= scope, lambda h,s: s[1]
var_decl_expr %= flux_control, lambda h,s: s[1]
var_decl_expr %= expression, lambda h,s: s[1]
var_decl_expr %= ocbracket + var_dec + ccbracket, lambda h,s: ParenthesisExpr(s[2])
var_decl_expr %= var_dec, lambda h,s: s[1]

vat_init_list %= var_init, lambda h,s: [s[1]]
vat_init_list %= var_init + comma + vat_init_list, lambda h,s: [s[1]] + s[3]

var_init %= identifier + inicialization + expression, lambda h,s: lambda h,s: VarDeclarationNode(s[1], s[3])

id_list %= identifier, lambda h,s: [s[1]]
id_list %= identifier + comma + id_list, lambda h,s: [s[1]] + s[3]

identifier %= id, lambda h,s: s[1]
identifier %= fully_typed_param, lambda h,s: s[1]

fully_typed_param %= id + type_anotation, lambda h,s: s[1] 

type_anotation %= type_assignation + id, lambda h,s: TypeAnotationNode(s[2]) 

scope %= obracket+inst_list+ cbracket, lambda h,s: BlockNode(s[2])

expression %= aritmetic_operation, lambda h,s: s[1]

expression %= atom + string_operator + expression, lambda h,s: StringSimpleConcatNode(s[1], s[3])
expression %= atom + string_operator_space + expression, lambda h,s: StringSpaceConcatNode(s[1], s[3])
expression %= var_asign, lambda h,s: s[1]

aritmetic_operation %= term + plus + aritmetic_operation, lambda h,s: PlusNode(s[1], s[3])
aritmetic_operation %= term + minus + aritmetic_operation, lambda h,s: MinusNode(s[1], s[3])
aritmetic_operation %= term, lambda h,s: s[1]

term %= factor + multiplication + term, lambda h,s: StarNode(s[1], s[3])
term %= factor + division + term, lambda h,s: DivNode(s[1], s[3])
term %= factor, lambda h,s: s[1]

factor %= factor + exponential + base_exponent, lambda h,s: PowNode(s[1], s[3])
factor %= base_exponent, lambda h,s: s[1]

base_exponent %= atom, lambda h,s: s[1]
base_exponent %= ocbracket + aritmetic_operation + ccbracket, lambda h,s: ParenthesisExpr(s[2])

atom %= number, lambda h,s: NumberNode(s[1])
atom %= function_call, lambda h,s: s[1]
atom %= var_use, lambda h,s: s[1]
atom %= vector, lambda h,s: s[1]
atom %= var_method, lambda h,s: s[1]
atom %= string_, lambda h,s: StringNode(s[1])
atom %= type_instanciation, lambda h,s: s[1]
atom %= boolean_value, lambda h,s: s[1]

var_asign %= var_use + assignation + expression, lambda h,s: VarAssignation(s[1], s[3])

function_declaration %= func_decl_id + ocbracket + id_list+ ccbracket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
function_declaration %= func_decl_id + ocbracket + ccbracket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])
function_declaration %= func_decl_id + ocbracket + id_list+ ccbracket + function_full_declaration + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
function_declaration %= func_decl_id + ocbracket + ccbracket + function_full_declaration + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])

function_declaration %= func_decl_id + ocbracket + id_list+ ccbracket + function_inline_declaration, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[5])
function_declaration %= func_decl_id + ocbracket + ccbracket + function_inline_declaration, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[4])

func_decl_id %= function + id, lambda h,s: s[2]

function_full_declaration %= scope, lambda h,s: s[1]
function_full_declaration %= type_anotation + scope, lambda h,s: s[2]

function_inline_declaration %= function_arrow + expression +semicolon, lambda h,s: s[2]
function_inline_declaration %= type_anotation + function_arrow + expression + semicolon, lambda h,s: s[3]

conditional %= if_ + inline_conditional,lambda h,s : s[1]
conditional %= if_ + full_conditional, lambda h,s :s[1]

inline_conditional %=  ocbracket + conditional_expresssion + ccbracket + expression + else_statement, lambda h,s: IfNode(s[2], s[4], s[5])
full_conditional %= ocbracket + conditional_expresssion + ccbracket + scope + else_statement, lambda h,s: IfNode(s[2], s[4], s[5])

else_statement %= elif_ + inline_conditional ,lambda h,s:s[1]
else_statement %= elif_ +full_conditional,lambda h,s:s[1]

else_statement %= else_ + inline_else, lambda h,s: s[2]
else_statement %= else_ + full_else, lambda h,s: s[2]

inline_else %= expression, lambda h,s: s[1]
full_else %= scope, lambda h,s: s[1]

while_loop %= while_ + ocbracket + conditional_expresssion + ccbracket + scope, lambda h,s: WhileLoopNode(s[3], s[5])

for_loop %= for_ + ocbracket + identifier + in_ + expression + ccbracket + scope, lambda h,s: ForLoopNode(s[3], s[5], s[7])

conditional_expresssion %= condition + logical_and + conditional_expresssion, lambda h,s: AndNode(s[1], s[3])
conditional_expresssion %= condition + logical_or + conditional_expresssion, lambda h,s: OrNode(s[1], s[3])
conditional_expresssion %= logical_not + condition, lambda h,s: NotNode(s[2])
conditional_expresssion %= condition, lambda h,s: s[1]

condition %= comparation, lambda h,s: s[1]
condition %= ocbracket + conditional_expresssion + ccbracket, lambda h,s: ParenthesisExpr(s[2])
comparation %= expression + comparator_greater + expression, lambda h,s: GreaterThatNode(s[1], s[3])
comparation %= expression + comparator_less + expression, lambda h,s: LessThatNode(s[1], s[3])
comparation %= expression + comparator_greater_equal + expression, lambda h,s: GreaterOrEqualThatNode(s[1], s[3])
comparation %= expression + comparator_less_equal + expression, lambda h,s: LessOrEqualThatNode(s[1], s[3])
comparation %= expression + comparator_equal + expression, lambda h,s: EqualNode(s[1], s[3])

boolean_value %= boolean_true, lambda h,s: BooleanNode(s[1])
boolean_value %= boolean_false, lambda h,s: BooleanNode(s[1])

type_declaration %= type_ + id + constructor + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[4])

type_declaration %= type_ + id + constructor + inherits_type + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])
type_declaration %= type_ + id + constructor + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], [])
type_declaration %= type_ + id + constructor + inherits_type + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])

constructor %= ocbracket + param_list + ccbracket, lambda h,s: s[2]
constructor %= ocbracket + ccbracket, lambda h,s: []
constructor %= G.Epsilon, lambda h,s: []

inherits_type %= inherits + id + constructor, lambda h,s: TypeInheritNode(s[2], s[3])

decl_body %= obracket+ cbracket, lambda h,s: []
decl_body %= obracket+ decl_list +  cbracket, lambda h,s: s[2]

decl_list %= decl + semicolon, lambda h,s: [s[1]]
decl_list %= decl + semicolon+decl_list, lambda h,s: [s[1]] + s[3]

decl %= atribute_declaration, lambda h,s: s[1]
decl %= method_declaration, lambda h,s: s[1]

atribute_declaration %= identifier + inicialization + expression, lambda h,s: AttrDeclarationNode(s[1], None, s[3])

method_declaration %= id + ocbracket + id_list + ccbracket + function_arrow + expression, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[6])
method_declaration %= id + ocbracket + id_list + ccbracket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])

method_declaration %= id + ocbracket + ccbracket + function_arrow + expression, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[5])
method_declaration %= id + ocbracket + ccbracket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])

function_call %= id + ocbracket + param_list + ccbracket, lambda h,s: CallNode(s[1], s[3])
function_call %= id + ocbracket + ccbracket, lambda h,s: CallNode(s[1], [])

type_instanciation %= new_ + id + ocbracket + param_list + ccbracket, lambda h,s: InstantiateTypeNode(s[2], s[4])
type_instanciation %= new_ + id + ocbracket + ccbracket, lambda h,s: InstantiateTypeNode(s[2], [])

param_list %= param, lambda h,s: [s[1]]
param_list %= param + comma + param_list, lambda h,s: [s[1]] + s[3]

param %= expression, lambda h,s: s[1]

var_use %= id, lambda h,s: VariableNode(s[1])
var_use %= atom + osbracket + expression + csbracket, lambda h,s: VecInstNode(s[1], s[3])
var_use %= var_attr, lambda h,s: s[1]

var_attr %= id + dot_ + id, lambda h,s: CallTypeAttr(s[1], s[3])
var_attr %= id + dot_ + var_attr, lambda h,s: CallTypeAttr(s[1], s[3])

var_method %= id + dot_ + function_call, lambda h,s: CallTypeFunc(s[1], s[3])

flux_control %= while_loop, lambda h,s: s[1]
flux_control %= conditional, lambda h,s: s[1]
flux_control %= for_loop, lambda h,s: s[1]

protocol_declaration %= protocol + id + protocol_body, lambda h,s: ProtocolNode(s[2], s[3])
protocol_declaration %= protocol + id + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[3])
protocol_declaration %= protocol + id + extends + id + protocol_body, lambda h,s: ProtocolNode(s[2], s[5], s[4])
protocol_declaration %= protocol + id + extends + id + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[5], s[4])

protocol_body %= obracket+virtual_method_list+ cbracket, lambda h,s: s[2]

virtual_method_list %= virtual_method + semicolon, lambda h,s: s[1]
virtual_method_list %= virtual_method + semicolon + virtual_method_list, lambda h,s: [s[1]] + s[3]

virtual_method %= id + ocbracket + ccbracket + type_anotation, lambda h,s: ProtocolMethod(s[1], s[4], [])
virtual_method %= id + ocbracket + fully_typed_params + ccbracket + type_anotation, lambda h,s: ProtocolMethod(s[1], s[5], s[3])

fully_typed_params %= fully_typed_param, lambda h,s: s[1]
fully_typed_params %= fully_typed_param + comma + fully_typed_params, lambda h,s: [s[1]] + s[3]

vector %= osbracket + vector_decl + csbracket, lambda h,s: VecDecExplSyntaxNode(s[2])

vector_decl %= param_list, lambda h,s: s[1]
vector_decl %= expression + gen_pattern_symbol + identifier + in_ + expression, lambda h,s: VecDecImplSyntaxNode(s[1], s[3], s[5])
#endregion

#region: SYMBOLS

DIGITS = '|'.join(str(i) for i in range(0, 10))
NONZERODIGITS = '|'.join(str(i) for i  in range(1, 10))
LOWERS = '|'.join(chr(i) for i in range(ord('a'), ord('z') + 1))
UPPERS = '|'.join(chr(i) for i in range(ord('A'), ord('Z') + 1))

IDENTIFIER = f'({UPPERS}|{LOWERS}|_)({UPPERS}|{LOWERS}|{DIGITS}|_)*'

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

INTEGER = f'({DIGITS})(.|{EPSILON})({DIGITS})*'

printables = '|'.join([printable for printable in list(map(mapping,string.printable))])
STRINGS_VALUES = f'(\")({printables})*(\")'

SPACE = '(\n|\t|\f|\r|\v| )(\n|\t|\f|\r|\v| )*'
#endregion
