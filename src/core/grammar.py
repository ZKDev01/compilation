import string

from tools.cmp.pycompiler import Grammar
from tools.regex import EPSILON
from tools.ast import * 

G = Grammar()
program = G.NonTerminal('<program>', True)

#region: NON-TERMINALS
instr_list = G.NonTerminal('<inst-list>')
param = G.NonTerminal('<param>')
program_level_decl_list = G.NonTerminal('<program-decl-list>')
program_level_decl = G.NonTerminal('<program-level-decl>')
instr_wrapper = G.NonTerminal('<inst-wrapper>')
instr = G.NonTerminal('<inst>')
var_dec = G.NonTerminal('<var-dec>')
expr = G.NonTerminal('<expression>')
flux_control = G.NonTerminal('<flux-control>')
base_exponent = G.NonTerminal('<base-exponent>')
scope = G.NonTerminal('<scope>')
func_decl = G.NonTerminal('<function-declaration>')
func_call = G.NonTerminal('<function-call>')
type_decl = G.NonTerminal('<type-declaration>')
id_list = G.NonTerminal('<id-list>')
type_inst = G.NonTerminal('<type-instanciation>')
var_asig = G.NonTerminal('<var-asign>')
arit_oper = G.NonTerminal('<aritmetic-operation>')
factor = G.NonTerminal('<factor>')
term = G.NonTerminal('<term>')
atom = G.NonTerminal('<atom>')
var_init = G.NonTerminal('<var-init>')
var_init_list = G.NonTerminal('<vat-init-list>')
string_oper =G.NonTerminal('<string-operation>')
string_atom = G.NonTerminal('<string-atom>')
func_full_decl = G.NonTerminal('<function-full-declaration>')
func_inline_decl = G.NonTerminal('<function-inline-declaration>')
var_decl_expression = G.NonTerminal('<var-decl-expr>')
conditional = G.NonTerminal('<conditional>')
inline_cond = G.NonTerminal('<inline-conditional>')
full_cond = G.NonTerminal('<full-conditional>')
else_stat = G.NonTerminal('<else-statement>')
inline_else = G.NonTerminal('<inline-else>')
full_else = G.NonTerminal('<full-else>')
loop = G.NonTerminal('<loop>')
while_loop = G.NonTerminal('<while-loop>')
for_loop = G.NonTerminal('<for-loop>')
iter_expr = G.NonTerminal('<iterable-expression>')
cond_expr = G.NonTerminal('<conditional-expresssion>')
condition = G.NonTerminal('<condition>')
bool_val = G.NonTerminal('<boolean-value>') 
comp = G.NonTerminal('<comparation>')
decl_body = G.NonTerminal('<decl-body>')
decl_list = G.NonTerminal('<decl-list>')
decl = G.NonTerminal('<decl>')
constructor = G.NonTerminal('<constructor>')
attr_decl = G.NonTerminal('<atribute-declaration>')
method_decl = G.NonTerminal('<method-declaration>')
func_call = G.NonTerminal('<function-call>')
param_list = G.NonTerminal('<param-list>')
var_attr = G.NonTerminal('<var-attr>')
var_method = G.NonTerminal('<var-method>')
id = G.NonTerminal('<identifier>')
type_anotation = G.NonTerminal('<type-anotation>')
protocol_decl =G.NonTerminal('<protocol-declaration>')
var_use = G.NonTerminal('<var-use>')
protocol_body = G.NonTerminal('<protocol-body>')
extend_ = G.NonTerminal('<extend-definer>')
virtual_method_list = G.NonTerminal('<virtual-method-list>')
virtual_method = G.NonTerminal('<virtual-method>')
fully_typed_params = G.NonTerminal('<fully-typed-params>')
fully_typed_param = G.NonTerminal('<fully-typed-param>')
vec = G.NonTerminal('<vector>')
vec_decl = G.NonTerminal('<vector-decl>')
gen_pattern = G.NonTerminal('<generation-pattern>')
func_decl_id = G.NonTerminal('<func-decl-id>')
inherits_type = G.NonTerminal('<inherits-type>')
#endregion

#region: TERMINALS
semicolon = G.Terminal(';')
gen_pattern_symbol = G.Terminal('||')
while_ = G.Terminal('while')
for_ = G.Terminal('for')
open_bracket = G.Terminal('{')
closed_bracket = G.Terminal('}')
let = G.Terminal('let')
ID = G.Terminal('ID')
assign = G.Terminal(':=')
init = G.Terminal('=')
in_ = G.Terminal('in')
inherits = G.Terminal('inherits')
comma = G.Terminal(',')
number = G.Terminal('number')
open_par = G.Terminal('(')
closed_par = G.Terminal(')')
plus_ = G.Terminal('+')
minus_ = G.Terminal('-')
mult = G.Terminal('*')
div = G.Terminal('/')
module_oper = G.Terminal('%')
string_= G.Terminal('string')
string_oper = G.Terminal('@')
string_oper_space = G.Terminal('@@')
func = G.Terminal('function')
func_arrow = G.Terminal('=>')
if_ = G.Terminal('if')
elif_ = G.Terminal('elif')
else_ = G.Terminal('else')
and_ = G.Terminal('&')
or_ = G.Terminal('|')
not_ = G.Terminal('!')

true = G.Terminal('true')
false = G.Terminal('false')

gt = G.Terminal('>')
lt = G.Terminal('<')
gte = G.Terminal('>=')
lte = G.Terminal('<=')
eq = G.Terminal('==')
neq = G.Terminal('!=')

new = G.Terminal('new')
type = G.Terminal('type')
dot = G.Terminal('.')

type_asignator = G.Terminal(':')
exponentiation = G.Terminal('^')

protocol = G.Terminal('protocol')
extends = G.Terminal('extends')

open_square_braket = G.Terminal('[')
close_square_braket = G.Terminal(']')
#endregion

#region: PRODUCTIONS
program %= program_level_decl_list, lambda h,s: ProgramNode(s[1])

program_level_decl_list%= instr_wrapper, lambda h,s: [s[1]]
program_level_decl_list %= program_level_decl + program_level_decl_list, lambda h,s: [s[1]] + s[2]
program_level_decl_list %= G.Epsilon, lambda h,s: []

program_level_decl %= type_decl, lambda h,s: s[1]
program_level_decl %= func_decl, lambda h,s: s[1]
program_level_decl %= protocol_decl, lambda h,s: s[1]

instr_list %= instr + semicolon, lambda h,s: [s[1]]
instr_list %= instr + semicolon + instr_list, lambda h,s: [s[1]] + s[3]

instr_wrapper %= instr, lambda h,s: s[1]
instr_wrapper %= instr + semicolon, lambda h,s: s[1]

instr %= scope, lambda h,s: s[1]
instr %= flux_control, lambda h,s: s[1]

instr %= expr, lambda h,s: s[1]
instr %= var_dec, lambda h,s: s[1]

var_dec %= let + var_init_list+ in_ + var_decl_expression, lambda h,s: VarsDeclarationsListNode(s[2], s[4])

var_decl_expression %= scope, lambda h,s: s[1]
var_decl_expression %= flux_control, lambda h,s: s[1]
var_decl_expression %= expr, lambda h,s: s[1]
var_decl_expression %= open_par + var_dec + closed_par, lambda h,s: ParenthesisExpr(s[2])
var_decl_expression %= var_dec, lambda h,s: s[1]

var_init_list %= var_init, lambda h,s: [s[1]]
var_init_list %= var_init + comma + var_init_list, lambda h,s: [s[1]] + s[3]

var_init %= id + init + expr, lambda h,s: lambda h,s: VarDeclarationNode(s[1], s[3])

id_list %= id, lambda h,s: [s[1]]
id_list %= id + comma + id_list, lambda h,s: [s[1]] + s[3]

id %= ID, lambda h,s: s[1]
id %= fully_typed_param, lambda h,s: s[1]

fully_typed_param %= ID + type_anotation, lambda h,s: s[1] 

type_anotation %= type_asignator + ID, lambda h,s: TypeAnotationNode(s[2]) 

scope%=open_bracket+instr_list+closed_bracket, lambda h,s: BlockNode(s[2])

expr %= arit_oper, lambda h,s: s[1]

expr %= atom + string_oper + expr, lambda h,s: StringSimpleConcatNode(s[1], s[3])
expr %= atom + string_oper_space + expr, lambda h,s: StringSpaceConcatNode(s[1], s[3])
expr %= var_asig, lambda h,s: s[1]

arit_oper %= term +plus_+ arit_oper, lambda h,s: PlusNode(s[1], s[3])
arit_oper %= term + minus_ + arit_oper, lambda h,s: MinusNode(s[1], s[3])
arit_oper %= term, lambda h,s: s[1]

term %= factor + mult + term, lambda h,s: StarNode(s[1], s[3])
term %= factor + div + term, lambda h,s: DivNode(s[1], s[3])
term %= factor, lambda h,s: s[1]

factor %= factor + exponentiation + base_exponent, lambda h,s: PowNode(s[1], s[3])
factor %= base_exponent, lambda h,s: s[1]

base_exponent %= atom, lambda h,s: s[1]
base_exponent %= open_par + arit_oper + closed_par, lambda h,s: ParenthesisExpr(s[2])

atom %= number, lambda h,s: NumberNode(s[1])
atom %= func_call, lambda h,s: s[1]
atom %= var_use, lambda h,s: s[1]
atom %= vec, lambda h,s: s[1]
atom %= var_method, lambda h,s: s[1]
atom %= string_, lambda h,s: StringNode(s[1])
atom %= type_inst, lambda h,s: s[1]
atom %= bool_val, lambda h,s: s[1]

var_asig %= var_use + assign + expr, lambda h,s: VarAssignation(s[1], s[3])

func_decl %= func_decl_id+open_par +id_list+ closed_par + func_full_decl, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
func_decl %= func_decl_id+open_par + closed_par + func_full_decl, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])
func_decl %= func_decl_id+open_par +id_list+ closed_par + func_full_decl + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
func_decl %= func_decl_id+open_par + closed_par + func_full_decl + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])

func_decl %= func_decl_id+open_par +id_list+ closed_par + func_inline_decl, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[5])
func_decl %= func_decl_id+open_par + closed_par + func_inline_decl, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[4])

func_decl_id %= func + ID, lambda h,s: s[2]

func_full_decl %= scope, lambda h,s: s[1]
func_full_decl %= type_anotation + scope, lambda h,s: s[2]

func_inline_decl %= func_arrow + expr +semicolon, lambda h,s: s[2]
func_inline_decl %= type_anotation + func_arrow + expr + semicolon, lambda h,s: s[3]

conditional %= if_ + inline_cond,lambda h,s : s[1]
conditional %= if_ + full_cond, lambda h,s :s[1]

inline_cond %=  open_par + cond_expr + closed_par + expr + else_stat, lambda h,s: IfNode(s[2], s[4], s[5])
full_cond %= open_par + cond_expr + closed_par + scope + else_stat, lambda h,s: IfNode(s[2], s[4], s[5])

else_stat %= elif_ + inline_cond ,lambda h,s:s[1]
else_stat %= elif_ +full_cond,lambda h,s:s[1]

else_stat %= else_ + inline_else, lambda h,s: s[2]
else_stat %= else_ + full_else, lambda h,s: s[2]

inline_else %= expr, lambda h,s: s[1]
full_else %= scope, lambda h,s: s[1]

while_loop %= while_ + open_par + cond_expr + closed_par + scope, lambda h,s: WhileLoopNode(s[3], s[5])

for_loop %= for_ + open_par + id + in_ + expr + closed_par + scope, lambda h,s: ForLoopNode(s[3], s[5], s[7])

cond_expr %= condition + and_ + cond_expr, lambda h,s: AndNode(s[1], s[3])
cond_expr %= condition + or_ + cond_expr, lambda h,s: OrNode(s[1], s[3])
cond_expr %= not_ + condition, lambda h,s: NotNode(s[2])
cond_expr %= condition, lambda h,s: s[1]

condition %= comp, lambda h,s: s[1]
condition %= open_par + cond_expr + closed_par, lambda h,s: ParenthesisExpr(s[2])
comp %= expr + gt + expr, lambda h,s: GreaterThatNode(s[1], s[3])
comp %= expr + lt + expr, lambda h,s: LessThatNode(s[1], s[3])
comp %= expr + gte + expr, lambda h,s: GreaterOrEqualThatNode(s[1], s[3])
comp %= expr + lte + expr, lambda h,s: LessOrEqualThatNode(s[1], s[3])
comp %= expr + eq + expr, lambda h,s: EqualNode(s[1], s[3])

bool_val %= true, lambda h,s: BooleanNode(s[1])
bool_val %= false, lambda h,s: BooleanNode(s[1])

type_decl %= type + ID + constructor + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[4])

type_decl %= type + ID + constructor + inherits_type + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])
type_decl %= type + ID + constructor + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], [])
type_decl %= type + ID + constructor + inherits_type + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])

constructor %= open_par + param_list + closed_par, lambda h,s: s[2]
constructor %= open_par + closed_par, lambda h,s: []
constructor %= G.Epsilon, lambda h,s: []

inherits_type %= inherits + ID + constructor, lambda h,s: TypeInheritNode(s[2], s[3])

decl_body %= open_bracket+closed_bracket, lambda h,s: []
decl_body %= open_bracket+ decl_list + closed_bracket, lambda h,s: s[2]

decl_list %= decl + semicolon, lambda h,s: [s[1]]
decl_list %= decl + semicolon+decl_list, lambda h,s: [s[1]] + s[3]

decl %= attr_decl, lambda h,s: s[1]
decl %= method_decl, lambda h,s: s[1]

attr_decl %= id + init + expr, lambda h,s: AttrDeclarationNode(s[1], None, s[3])

method_decl %= ID + open_par + id_list + closed_par + func_arrow + expr, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[6])
method_decl %= ID + open_par + id_list + closed_par + func_full_decl, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])

method_decl %= ID + open_par + closed_par + func_arrow + expr, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[5])
method_decl %= ID + open_par + closed_par + func_full_decl, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])

func_call %= ID + open_par + param_list + closed_par, lambda h,s: CallNode(s[1], s[3])
func_call %= ID + open_par + closed_par, lambda h,s: CallNode(s[1], [])

type_inst %= new + ID + open_par + param_list + closed_par, lambda h,s: InstantiateTypeNode(s[2], s[4])
type_inst %= new + ID + open_par + closed_par, lambda h,s: InstantiateTypeNode(s[2], [])

param_list %= param, lambda h,s: [s[1]]
param_list %= param + comma + param_list, lambda h,s: [s[1]] + s[3]

param %= expr, lambda h,s: s[1]

var_use %= ID, lambda h,s: VariableNode(s[1])
var_use %= atom+open_square_braket+expr+close_square_braket, lambda h,s: VecInstNode(s[1], s[3])
var_use %= var_attr, lambda h,s: s[1]

var_attr %= ID + dot + ID, lambda h,s: CallTypeAttr(s[1], s[3])
var_attr %= ID + dot + var_attr, lambda h,s: CallTypeAttr(s[1], s[3])

var_method %= ID + dot + func_call, lambda h,s: CallTypeFunc(s[1], s[3])

flux_control %= while_loop, lambda h,s: s[1]
flux_control %= conditional, lambda h,s: s[1]
flux_control %= for_loop, lambda h,s: s[1]

protocol_decl %= protocol + ID + protocol_body, lambda h,s: ProtocolNode(s[2], s[3])
protocol_decl %= protocol + ID + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[3])
protocol_decl %= protocol + ID + extends + ID + protocol_body, lambda h,s: ProtocolNode(s[2], s[5], s[4])
protocol_decl %= protocol + ID + extends + ID + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[5], s[4])

protocol_body %= open_bracket+virtual_method_list+closed_bracket, lambda h,s: s[2]

virtual_method_list %= virtual_method + semicolon, lambda h,s: s[1]
virtual_method_list %= virtual_method + semicolon + virtual_method_list, lambda h,s: [s[1]] + s[3]

virtual_method %= ID + open_par+closed_par + type_anotation, lambda h,s: ProtocolMethod(s[1], s[4], [])
virtual_method %= ID + open_par+fully_typed_params+closed_par + type_anotation, lambda h,s: ProtocolMethod(s[1], s[5], s[3])

fully_typed_params %= fully_typed_param, lambda h,s: s[1]
fully_typed_params %= fully_typed_param + comma + fully_typed_params, lambda h,s: [s[1]] + s[3]

vec %= open_square_braket + vec_decl + close_square_braket, lambda h,s: VecDecExplSyntaxNode(s[2])

vec_decl %= param_list, lambda h,s: s[1]
vec_decl %= expr + gen_pattern_symbol + id + in_ + expr, lambda h,s: VecDecImplSyntaxNode(s[1], s[3], s[5])
#endregion