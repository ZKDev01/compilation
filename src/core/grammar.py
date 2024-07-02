from tools.cmp.pycompiler import Grammar
from tools.ast import * # TODO: hacer ast

G = Grammar()
program = G.NonTerminal('<program>', True)


#non terminals
#region 
instr_list = G.NonTerminal('<inst-list>')
param = G.NonTerminal('<param>')
program_level_decl_list = G.NonTerminal('<program-decl-list>')
program_level_decl = G.NonTerminal('<program-level-decl>')
instr_wrapper = G.NonTerminal('<inst-wrapper>')
instr = G.NonTerminal('<inst>')
var_dec = G.NonTerminal('<var-dec>')
exp = G.NonTerminal('<expression>')
flux_control = G.NonTerminal('<flux-control>')
exponent = G.NonTerminal('<base-exponent>')
scope = G.NonTerminal('<scope>')
func_decl = G.NonTerminal('<function-declaration>')
function_call = G.NonTerminal('<function-call>')
type_declaration = G.NonTerminal('<type-declaration>')
id_list = G.NonTerminal('<id-list>')
type_instanciation = G.NonTerminal('<type-instanciation>')
var_asign = G.NonTerminal('<var-asign>')
arit_exp = G.NonTerminal('<aritmetic-operation>')
factor = G.NonTerminal('<factor>')
term = G.NonTerminal('<term>')
atom = G.NonTerminal('<atom>')
var_init = G.NonTerminal('<var-init>')
var_init_list = G.NonTerminal('<vat-init-list>')
string_operation =G.NonTerminal('<string-operation>')
string_atom = G.NonTerminal('<string-atom>')
function_full_declaration = G.NonTerminal('<function-full-declaration>')
function_inline_declaration = G.NonTerminal('<function-inline-declaration>')
var_decl_exp = G.NonTerminal('<var-decl-expr>')
conditional = G.NonTerminal('<conditional>')
inline_conditional = G.NonTerminal('<inline-conditional>')
full_conditional = G.NonTerminal('<full-conditional>')
else_statement = G.NonTerminal('<else-statement>')
inline_else = G.NonTerminal('<inline-else>')
full_else = G.NonTerminal('<full-else>')
loop = G.NonTerminal('<loop>')
while_loop = G.NonTerminal('<while-loop>')
for_loop = G.NonTerminal('<for-loop>')
iterable_expression = G.NonTerminal('<iterable-expression>')
cond_exp = G.NonTerminal('<conditional-expresssion>')
cond = G.NonTerminal('<condition>')
boolean_value = G.NonTerminal('<boolean-value>') 
comparation = G.NonTerminal('<comparation>')
decl_body = G.NonTerminal('<decl-body>')
decl_list = G.NonTerminal('<decl-list>')
declaration = G.NonTerminal('<decl>')
constructor = G.NonTerminal('<constructor>')
atribute_declaration = G.NonTerminal('<atribute-declaration>')
method_declaration = G.NonTerminal('<method-declaration>')
function_call = G.NonTerminal('<function-call>')
param_list = G.NonTerminal('<param-list>')
var_attr = G.NonTerminal('<var-attr>')
var_method = G.NonTerminal('<var-method>')
var_id = G.NonTerminal('<identifier>')
type_anotation = G.NonTerminal('<type-anotation>')
protocol_decl =G.NonTerminal('<protocol-declaration>')
var_use = G.NonTerminal('<var-use>')
protocol_body = G.NonTerminal('<protocol-body>')
extend_definer = G.NonTerminal('<extend-definer>')
virtual_method_list = G.NonTerminal('<virtual-method-list>')
virtual_method = G.NonTerminal('<virtual-method>')
fully_typed_params = G.NonTerminal('<fully-typed-params>')
typed_param = G.NonTerminal('<fully-typed-param>')
vector = G.NonTerminal('<vector>')
vector_decl = G.NonTerminal('<vector-decl>')
generation_pattern = G.NonTerminal('<generation-pattern>')
func_decl_id = G.NonTerminal('<func-decl-id>')
inherits_type = G.NonTerminal('<inherits-type>')
#endregion

#terminals
#region
semicolon = G.Terminal(';')
gen_pattern_symbol = G.Terminal('||')
while_ = G.Terminal('while')
for_ = G.Terminal('for')
open_bracket = G.Terminal('{')
closed_bracket = G.Terminal('}')
let = G.Terminal('let')
ID = G.Terminal('ID')
asignation = G.Terminal(':=')
inicialization = G.Terminal('=')
in_ = G.Terminal('in')
inherits = G.Terminal('inherits')
comma = G.Terminal(',')
number = G.Terminal('number')
open_par = G.Terminal('(')
closed_par = G.Terminal(')')
plus = G.Terminal('+')
minus = G.Terminal('-')
mult = G.Terminal('*')
div = G.Terminal('/')
module_operation = G.Terminal('%')
string_= G.Terminal('string')
string_oper = G.Terminal('@')
string_oper_space = G.Terminal('@@')
function = G.Terminal('function')
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
power = G.Terminal('^')

protocol = G.Terminal('protocol')
extends = G.Terminal('extends')

open_square_braket = G.Terminal('[')
close_square_braket = G.Terminal(']')
#endregion

#productions
#region

#<program> -> <instr-list>
program %= program_level_decl_list, lambda h,s: ProgramNode(s[1]) #TODO verificar

program_level_decl_list%= instr_wrapper, lambda h,s: [s[1]]
program_level_decl_list %= program_level_decl + program_level_decl_list, lambda h,s: [s[1]] + s[2]
program_level_decl_list %= G.Epsilon, lambda h,s: []

program_level_decl %= type_declaration, lambda h,s: s[1]
program_level_decl %= func_decl, lambda h,s: s[1]
program_level_decl %= protocol_decl, lambda h,s: s[1]

#intruction list
#<instr-list> -> <instr>; | <instr>; <instr-list>
instr_list %= instr + semicolon, lambda h,s: [s[1]]
instr_list %= instr + semicolon + instr_list, lambda h,s: [s[1]] + s[3]

instr_wrapper %= instr, lambda h,s: s[1]
instr_wrapper %= instr + semicolon, lambda h,s: s[1]

#instruction
#<instr> -> <var-dec> | <func-call> | <func-dec> | <type-dec> | <scope> | <flux-control> | <var-asign> | <expression>
instr %= scope, lambda h,s: s[1]
instr %= flux_control, lambda h,s: s[1]
instr %= exp, lambda h,s: s[1]
instr %= var_dec, lambda h,s: s[1]

#var declaration 
#<var-dec> -> let <var-init-list> in <var-decl-expression> 
var_dec %= let + var_init_list + in_ + var_decl_exp, lambda h,s: VarsDeclarationsListNode(s[2], s[4])

#var declaration expression 
# <var-decl-expression> -> <scope> | <flux-control> | <var-decl> | <expression> | (<var-dec>)
var_decl_exp %= scope, lambda h,s: s[1]
var_decl_exp %= flux_control, lambda h,s: s[1]
var_decl_exp %= exp, lambda h,s: s[1]
var_decl_exp %= open_par + var_dec + closed_par, lambda h,s: ParenthesisExpr(s[2])
var_decl_exp %= var_dec, lambda h,s: s[1]

#var-inicialization-list 
# <var-init-list> -> <var-init> | <var-init> , <var-init-list>
var_init_list %= var_init, lambda h,s: [s[1]]
var_init_list %= var_init + comma + var_init_list, lambda h,s: [s[1]] + s[3]

#var initialization 
# <var-init> -> ID = <expression> | ID = <var-asign>
var_init %= var_id + inicialization + exp, lambda h,s: lambda h,s: VarDeclarationNode(s[1], s[3])

# #id list 
# <id-list> -> <identifier> | <identifier>, <id-list>
id_list %= var_id, lambda h,s: [s[1]]
id_list %= var_id + comma + id_list, lambda h,s: [s[1]] + s[3]

#identifier <identifier> -> ID | ID <type-anotation>
var_id %= ID, lambda h,s: s[1]
var_id %= typed_param, lambda h,s: s[1]

#fullt typed param 
# <typed_param> -> 
typed_param %= ID + type_anotation, lambda h,s: s[1] #TODO: this has type

# #type anotation 
# <type-anotation> -> : Number
type_anotation %= type_asignator + ID, lambda h,s: TypeAnotationNode(s[2]) #TODO: this has type

#scopes
# <scope> -> { <inst-list> }
scope %= open_bracket + instr_list + closed_bracket, lambda h,s: BlockNode(s[2])

#expressions 
# <expresion> -> <aritmetic-op> | <type-instanciation> | <string-operation>
exp %= arit_exp, lambda h,s: s[1]
exp %= atom + string_oper + exp, lambda h,s: StringSimpleConcatNode(s[1], s[3])
exp %= atom + string_oper_space + exp, lambda h,s: StringSpaceConcatNode(s[1], s[3])
exp %= var_asign, lambda h,s: s[1]

#artimetic expresssion 
# <arit-exp> -> <factor> + <arit-exp> | <factor> - <arit-exp> | <factor>

arit_exp %= term + plus + arit_exp, lambda h,s: PlusNode(s[1], s[3])
arit_exp %= term + minus + arit_exp, lambda h,s: MinusNode(s[1], s[3])
arit_exp %= term, lambda h,s: s[1]

#factor 
# <factor> -> <atom> * <factor> | <atom> / <factor> | <atom>
term %= factor + mult + term, lambda h,s: StarNode(s[1], s[3])
term %= factor + div + term, lambda h,s: DivNode(s[1], s[3])
term %= factor, lambda h,s: s[1]

factor %= factor + power + exponent, lambda h,s: PowNode(s[1], s[3])
factor %= exponent, lambda h,s: s[1] #TODO revisar. Porq es exponent y no atom?

exponent %= atom, lambda h,s: s[1]
exponent %= open_par + arit_exp + closed_par, lambda h,s: ParenthesisExpr(s[2])

#atom 
# <atom> -> (<expression>) | number | <function-call> | id
atom %= number, lambda h,s: NumberNode(s[1])
atom %= function_call, lambda h,s: s[1]
atom %= var_use, lambda h,s: s[1]
atom %= vector, lambda h,s: s[1]
atom %= var_method, lambda h,s: s[1]
atom %= string_, lambda h,s: StringNode(s[1])
atom %= type_instanciation, lambda h,s: s[1]
atom %= boolean_value, lambda h,s: s[1]

#string_operation <string-operation> -> <string-atom> @ <string-operation> | <string-atom>
# string_operation %= string_atom
# string_operation %= string_atom + string_operator + string_operation
# string_operation %= string_atom + string_operator_space + string_operation

# #string_atom <string-atom> -> string_| <function-call> | ID
# string_atom %= string_
# string_atom %= function_call
# string_atom %= ID
# string_atom %= variable_atribute
# string_atom %= variable_method
# string_atom %= open_curly_braket + string_operation + closed_curly_braket

#variable asignation <var-asignation> ->  <var-use> := <expression>
var_asign %= var_use + asignation + exp, lambda h,s: VarAssignation(s[1], s[3])
# var_asignation %= var_use + asignation + var_asignation

#function declaration <function-declaration> -> <func-inline-declaration> | <func-full-dec>

func_decl %= func_decl_id + open_par + id_list + closed_par + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
func_decl %= func_decl_id + open_par + closed_par + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])
func_decl %= func_decl_id + open_par + id_list + closed_par + function_full_declaration + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
func_decl %= func_decl_id + open_par + closed_par + function_full_declaration + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])

func_decl %= func_decl_id+open_par +id_list+ closed_par + function_inline_declaration, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[5])
func_decl %= func_decl_id+open_par + closed_par + function_inline_declaration, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[4])

func_decl_id %= function + ID, lambda h,s: s[2]

#function full declaration 
# <function-full-declaration> -> function ID(<id-list>)<scope> | function ID()<scope>
function_full_declaration %= scope, lambda h,s: s[1]
function_full_declaration %= type_anotation + scope, lambda h,s: s[2] # TODO: this has type

#function inline declaration 
# <function-inline-declaration> -> function ID (<id-list> ) => <expression> | function ID () => <expression>
function_inline_declaration %= func_arrow + exp +semicolon, lambda h,s: s[2]
function_inline_declaration %= type_anotation + func_arrow + exp + semicolon, lambda h,s: s[3] # TODO: this has type

#conditional  
# <conditional> -> <inline-conditional> | <full-conditional>
conditional %= if_ + inline_conditional,lambda h,s : s[1]
conditional %= if_ + full_conditional, lambda h,s :s[1]

#inline conditional 
# <inline-conditional> -> if (<conditional-expression>) expression <else-staement>
inline_conditional %=  open_par + cond_exp + closed_par + exp + else_statement, lambda h,s: IfNode(s[2], s[4], s[5])
full_conditional %= open_par + cond_exp + closed_par + scope + else_statement, lambda h,s: IfNode(s[2], s[4], s[5])
#full conditional <full-conditional> -> if (<conditional>) { <instruction> } <else-statement>

else_statement %= elif_ + inline_conditional ,lambda h,s:s[1]
else_statement %= elif_ +full_conditional,lambda h,s:s[1]

else_statement %= else_ + inline_else, lambda h,s: s[2]
else_statement %= else_ + full_else, lambda h,s: s[2]

inline_else %= exp, lambda h,s: s[1]
full_else %= scope, lambda h,s: s[1]

#while instruction 
# <while-loop> -> while (<condition-expression>) <scope>
while_loop %= while_ + open_par + cond_exp + closed_par + scope, lambda h,s: WhileLoopNode(s[3], s[5])

#for instruction 
# <for-loop> -> for ( Id in <iterable-expression>) <scope> 
for_loop %= for_ + open_par + var_id + in_ + exp + closed_par + scope, lambda h,s: ForLoopNode(s[3], s[5], s[7])

#conditional expression <conditional-expression> -> <condition> & <conditiona-expression> | <condition> '|' <conditiona-expression> | !<condition> | <condition>
cond_exp %= cond + and_ + cond_exp, lambda h,s: AndNode(s[1], s[3])
cond_exp %= cond + or_ + cond_exp, lambda h,s: OrNode(s[1], s[3])
cond_exp %= not_ + cond, lambda h,s: NotNode(s[2])
cond_exp %= cond, lambda h,s: s[1]

#condition <condition> -> <boolean-value> | <comparation> | (<conditional_expression>) 
# condition %= boolean_value
cond %= comparation, lambda h,s: s[1]
cond %= open_par + cond_exp + closed_par, lambda h,s: ParenthesisExpr(s[2])

#comparation 
# <comparation> -> <expression> '>' <expression> | <expression> '<' <expression> | <expression> =< <expression> | <expression> >= <expression> | <expression> == <expression> | <expression> != <expression>
comparation %= exp + gt + exp, lambda h,s: GreaterThatNode(s[1], s[3])
comparation %= exp + lt + exp, lambda h,s: LessThatNode(s[1], s[3])
comparation %= exp + gte + exp, lambda h,s: GreaterOrEqualThatNode(s[1], s[3])
comparation %= exp + lte + exp, lambda h,s: LessOrEqualThatNode(s[1], s[3])
comparation %= exp + eq + exp, lambda h,s: EqualNode(s[1], s[3])
# comparation %= expression + neq + expression 

#boolean value 
# <boolean-value> -> true | false
boolean_value %= true, lambda h,s: BooleanNode(s[1])
boolean_value %= false, lambda h,s: BooleanNode(s[1])

#type declaration 
# <type-declaration> -> <type-declaration> -> type + <constructor> + <decl-body> | type<constructor>inherits <constructor><decl-body>
type_declaration %= type + ID + constructor + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[4])

type_declaration %= type + ID + constructor + inherits_type + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])
type_declaration %= type + ID + constructor + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], [])
type_declaration %= type + ID + constructor + inherits_type + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])

#constructor 
# <constructor> -> ID | ID()
constructor %= open_par + param_list + closed_par, lambda h,s: s[2]
constructor %= open_par + closed_par, lambda h,s: []
constructor %= G.Epsilon, lambda h,s: []

inherits_type %= inherits + ID + constructor, lambda h,s: TypeInheritNode(s[2], s[3])

#declaration body 
# <decl-body> -> {<decl-list>} | {}
decl_body %= open_bracket+closed_bracket, lambda h,s: []
decl_body %= open_bracket+ decl_list + closed_bracket, lambda h,s: s[2]

#declaration statement list 
# <decl-list> -> <declaration>; | <declaration>;<decl-list> 
decl_list %= declaration + semicolon, lambda h,s: [s[1]]
decl_list %= declaration + semicolon+decl_list, lambda h,s: [s[1]] + s[3]

#declaration 
# <declaration> -> <atribute-declaration> | <method-declaration>
declaration %= atribute_declaration, lambda h,s: s[1]
declaration %= method_declaration, lambda h,s: s[1]

#atribute declaration 
# <atribute-declaration> -> ID = <expression>
atribute_declaration %= var_id + inicialization + exp, lambda h,s: AttrDeclarationNode(s[1], None, s[3])

#method declaration 
# <method-declaration>-> ID (<params>) => <expression> | ID (<params>) => { <inst-list> } 
method_declaration %= ID + open_par + id_list + closed_par + func_arrow + exp, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[6])
method_declaration %= ID + open_par + id_list + closed_par + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])

method_declaration %= ID + open_par + closed_par + func_arrow + exp, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[5])
method_declaration %= ID + open_par + closed_par + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])

#function call 
# <func-call> -> ID(<param-list>) | ID()
function_call %= ID + open_par + param_list + closed_par, lambda h,s: CallNode(s[1], s[3])
function_call %= ID + open_par + closed_par, lambda h,s: CallNode(s[1], [])

#type instanciation 
# <type-instanciation -> new ID (<param-list>) | new ID()
type_instanciation %= new + ID + open_par + param_list + closed_par, lambda h,s: InstantiateTypeNode(s[2], s[4])
type_instanciation %= new + ID + open_par + closed_par, lambda h,s: InstantiateTypeNode(s[2], [])

#param list 
# <param-list> -> <expression> | <expression> , <param-list>
param_list %= param, lambda h,s: [s[1]]
param_list %= param + comma + param_list, lambda h,s: [s[1]] + s[3]

param %= exp, lambda h,s: s[1]

#var use <var-use> -> Id | <variable-atribute>
var_use %= ID, lambda h,s: VariableNode(s[1])
var_use %= atom + open_square_braket + exp + close_square_braket, lambda h,s: VecInstNode(s[1], s[3])
var_use %= var_attr, lambda h,s: s[1]

#variable atribute use 
# <var-atrr>-> ID.ID
var_attr %= ID + dot + ID, lambda h,s: CallTypeAttr(s[1], s[3])
var_attr %= ID + dot + var_attr, lambda h,s: CallTypeAttr(s[1], s[3])

#variable method use 
# <var-method> -> ID.ID(param_list) | ID.ID()
var_method %= ID + dot + function_call, lambda h,s: CallTypeFunc(s[1], s[3])

#flux controllers 
# <flux-control> -> <while> | if | for
flux_control %= while_loop, lambda h,s: s[1]
flux_control %= conditional, lambda h,s: s[1]
flux_control %= for_loop, lambda h,s: s[1]

#protocol declaration 
# <protocol-declaration> -> protocol <protocol-definer> <protocol-body>
protocol_decl %= protocol + ID + protocol_body, lambda h,s: ProtocolNode(s[2], s[3])
protocol_decl %= protocol + ID + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[3])
protocol_decl %= protocol + ID + extends + ID + protocol_body, lambda h,s: ProtocolNode(s[2], s[5], s[4])
protocol_decl %= protocol + ID + extends + ID + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[5], s[4])

#protocol body (type decl body with full typing) 
# <protocol-body> -> {<virtual-method-list>}
protocol_body %= open_bracket + virtual_method_list + closed_bracket, lambda h,s: s[2]

#virtual method list 
# <virtual-method-list> -> <virtual-method>;|<virtual-method>;<virtual-method-list>
virtual_method_list %= virtual_method + semicolon, lambda h,s: s[1]
virtual_method_list %= virtual_method + semicolon + virtual_method_list, lambda h,s: [s[1]] + s[3]

#virtual method 
# <virtual-method> -> ID():ID | ID(param_list_typed):ID
virtual_method %= ID + open_par + closed_par + type_anotation, lambda h,s: ProtocolMethod(s[1], s[4], [])
virtual_method %= ID + open_par + fully_typed_params + closed_par + type_anotation, lambda h,s: ProtocolMethod(s[1], s[5], s[3])

#param_list_typed 
# <param-list-typed> -> <typed-param> | <typed-param> , <param-list-typed>
fully_typed_params %= typed_param, lambda h,s: s[1]
fully_typed_params %= typed_param + comma + fully_typed_params, lambda h,s: [s[1]] + s[3]

#vectors
vector %= open_square_braket + vector_decl + close_square_braket, lambda h,s: VecDecExplSyntaxNode(s[2])

#vector declaration
vector_decl %= param_list, lambda h,s: s[1]
vector_decl %= exp + gen_pattern_symbol + var_id + in_ + exp, lambda h,s: VecDecImplSyntaxNode(s[1], s[3], s[5])



#endregion