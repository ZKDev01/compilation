from tools.ast import *
from tools.cmp import visitor
from tools.cmp.semantic import Scope, Context

class SemanticCheckerVisitor:

  def __init__(self):
    self.errors = []
    
  def clean_errors(self):
    self.errors = []

  @visitor.on("node")
  def visit(self, node,context:Context,scope: Scope):
    pass    
    
  @visitor.when(ProgramNode)
  def visit(self, node, context=None ,scope=None):
    scope = Scope()
    scope.define_variable('pi')
    scope.define_function('print',1)
    scope.define_function('sin',1)
    scope.define_function('cos',1)
    scope.define_function('tan',1)
    scope.define_function('pow',2)
    context = Context()
    print(len(node.statements))
    for statement in node.statements:
      self.visit(statement,context,scope)
    return self.errors
    
  @visitor.when(VarDeclarationNode)
  def visit(self, node,context, scope):
    scope.define_variable(node.id) 
    self.visit(node.expression,context,scope)
    
  @visitor.when(FuncFullDeclarationNode)
  def visit(self, node,context, scope):
    inner_scope =scope.create_child_scope()
    for n in node.params:
      inner_scope.define_variable(n)
    if scope.is_func_defined(node.id,len(node.params)):
      self.errors.append(f'function {node.id} already defined')
    else:
      scope.define_function(node.id,len(node.params))
    self.visit(node.body,context,inner_scope)
    
  @visitor.when(FuncInlineDeclarationNode)
  def visit(self, node,context, scope):        
    inner_scope =scope.create_child_scope()
    for n in node.params:
      inner_scope.define_variable(n)
    if scope.is_func_defined(node.id,len(node.params)):
      self.errors.append(f'function {node.id} already defined')
    else:
      scope.define_function(node.id,len(node.params))
    self.visit(node.body,context,inner_scope)

  @visitor.when(BinaryNode)
  def visit(self, node,context,scope):
    self.visit(node.left,context,scope)
    self.visit(node.right,context,scope)

  @visitor.when(BlockNode)
  def visit(self,node,context,scope):
    new_scope = scope.create_child_scope()
    for expr in node.exprs:
      self.visit(expr,context,new_scope)

  @visitor.when(CallNode)
  def visit(self, node, context ,scope):
    is_valid = scope.is_func_defined(node.id,len(node.args))
    if not is_valid:
      self.errors.append(f'function {node.id} is not defined')
      return
    for arg in node.args:
      self.visit(arg,context,scope)

  @visitor.when(VariableNode)
  def visit(self, node,context ,scope):
    if  isinstance(node.id,str):
      if not scope.is_var_defined(node.id):
        print(type(node),type(node.id),node.id)
        self.errors.append(f'variable not defined {node.id}')
    else:
      self.visit(node.id,context,scope)

  @visitor.when(VarAssignation)
  def visit(self,node,context,scope):
    if scope.is_var_defined(node.id):
      self.visit(node.expr,context,scope)
    else:
      self.errors.append(f'cannot asign to undefined var {node.id}')

  @visitor.when(VecDecExplSyntaxNode)
  def visit(self,node,context,scope):
    for arg in node.args:
      self.visit(arg,context,scope)

  @visitor.when(VecDecImplSyntaxNode)
  def visit (self,node,context,scope):
    new_scope = scope.create_child_scope()
    new_scope.define_variable(node.var.id)
    self.visit(node.expr,context,new_scope)

  @visitor.when(TypeDeclarationNode)
  def visit(self,node,context,scope):
    inner_scope = scope.create_child_scope()
    inner_scope.define_variable('self')
    context.create_type(node.id)
    if node.inherit :
      self.visit(node.inherit,context,inner_scope)

    for feature in node.features:
      self.visit(feature,context,inner_scope)
        
    for attr in inner_scope.local_vars:
      try:
        context.get_type(node.id).define_attribute(attr.name,'Any')
      except Exception as e:
        self.errors.append(e.message)

    for method in inner_scope.local_funcs:
      try:
        context.get_type(node.id).define_method(method.name,'Any','Any','Any')
      except Exception as e:
        self.errors.append(e.message)

  @visitor.when(CallTypeAttr)
  def visit(self,node,context,scope):
              self.visit(node.attr,context,scope)

  @visitor.when(TypeInheritNode)
  def visit(self,node,context,scope):
        try:
            scope.define_function('base',node.args)
            context.get_type(node.id)
        except:
            self.errors.append(f"cannot inherit from unexisting {node.id} type")

  @visitor.when(AttrDeclarationNode)
  def visit(self,node,context,scope):
        if scope.is_var_defined(node.id):
            self.errors.append(f'atribute duplication {node.id}')
            return
        scope.define_variable(node.id)
        child_scope = scope.create_child_scope()
        self.visit(node.expr,context,child_scope)

  @visitor.when(VecInstNode)
  def visit(self,node,context,scope):
        self.visit(node.var,context,scope)
        self.visit(node.index,context,scope)
    
  @visitor.when(InstantiateTypeNode)
  def visit(self,node,context,scope):
        try:
            context.get_type(node.id)
            for arg in node.args:
                self.visit(arg,context,scope)
        except:
            self.errors.append(f'type {node.id} not defined')

  @visitor.when(VarsDeclarationsListNode)
  def visit(self,node,context,scope):
        self.visit(node.declarations,context,scope)

  @visitor.when(VarDeclarationNode)
  def visit(self,node,context,scope):
        if isinstance(node.id,str):
            if scope.is_var_defined(node.id):
                self.errors.append(f'variable {node.id} already defined')
        else:
            print(node.type,node.attr)
        self.visit(node.expr,context,scope.create_child_scope())

  @visitor.when(VarAssignation)
  def visit(self,node,context,scope):
        if isinstance(node.id,str):
            if not scope.is_var_defined(node.id):
                self.errors.append(f'variable {node.id} is not defined')
        else:
            self.visit(node.id,context,scope)
        self.visit(node.expr,context,scope.create_child_scope())

  @visitor.when(WhileLoopNode)
  def visit(self,node,context,scope):
        self.visit(node.expr,context,scope)
        self.visit(node.body,context,scope)

  @visitor.when(IfNode)
  def visit(self,node,context,scope):
        self.visit(node.if_expr,context,scope.create_child_scope())
        self.visit(node.then_expr,context,scope,scope.create_child_scope())
        self.visit(node.else_expr,context,scope,scope.create_child_scope())

  @visitor.when(WhileLoopNode)
  def visit(self,node,context,scope):
        self.visit(node.if_expr)

  @visitor.when(CallTypeAttr)
  def visit(self,node,context,scope):
       if not scope.is_var_defined(node.type_id) or  not scope.is_local_var(node.attr):
          self.errors.append(f'atribute {node.type_id}.{node.attr} not defined') 

  @visitor.when(VecInstNode)
  def visit(self,node,context,scope):
        self.visit(node.var,context,scope)
        self.visit(node.index,context,scope)

  @visitor.when(ProtocolNode)
  def visit(self,node,context,scope):
        inner_scope = scope.create_child_scope()
        try:
         context.create_type(node.id)
        except:
            self.errors.append(f'invalid re declaration of {node.id} type')
        if node.extends is not None:
            self.visit(node.extends)
        for method in node.methods:
            self.visit(method,context,inner_scope)
        for method in inner_scope.local_funcs:
            try:
                context.get_type(node.id).define_method(method.name,'Any','Any','Any')
            except Exception as e:
                self.errors.append(e.message)

class TypeCheckingVisitor:
  def __init__(self):
        self.errors = []

  @visitor.on("node")
  def visit(self, node,context:Context):
        pass    

  @visitor.when(ProgramNode)
  def visit(self, node, context=None):
        context = Context()
        context.create_type('Number')
        context.create_type('Bool')
        context.create_type('String')
        context.create_type('Any')
        context.create_type('Void')
        context.create_type('Vec')

        for statement in node.statements:
                self.visit(statement,context)
        return self.errors
    
  @visitor.when(VarDeclarationNode)
  def visit(self, node,context):
        self.visit(node.expression,context)

  @visitor.when(FuncFullDeclarationNode)
  def visit(self, node,context):
        self.visit(node.body,context)
        self.visit(node.params,context)
    
  @visitor.when(FuncInlineDeclarationNode)
  def visit(self, node,context):        
        self.visit(node.body,context)
        self.visit(node.params,context)

  @visitor.when(BinaryNode)
  def visit(self, node,context):
        self.visit(node.left,context)
        self.visit(node.right,context)
        if node.left.type_of() != node.right.type_of():
            self.errors.append(f'mismatch types between {str(node.left)} {str(node.right)}')

  @visitor.when(BlockNode)
  def visit(self,node,context):
        for expr in node.exprs:
            self.visit(expr,context)


  @visitor.when(CallNode)
  def visit(self, node, context):
        for arg in node.args:
            self.visit(arg,context)
        try:
            type = context.get_type(node.id).atributes[0]
            node.set_type(type)
        except:
            pass

  @visitor.when(VariableNode)
  def visit(self, node,context):
        try:
            node.set_type(context.get_type(node.type_of()))
        except:
            pass

  @visitor.when(VarAssignation)
  def visit(self,node,context):
            self.visit(node.expr,context)

            if node.type_of() != node.expr.type_of():
                self.errors(f'no se puede asignar {node.type_of()} a {node.expr.type_of()}')

  @visitor.when(VecDecExplSyntaxNode)
  def visit(self,node,context):
          for arg in node.args:
              self.visit(arg,context)

  @visitor.when(VecDecImplSyntaxNode)
  def visit (self,node,context):
        self.visit(node.expr,context)

  @visitor.when(TypeDeclarationNode)
  def visit(self,node,context):
        if node.inherit :
            self.visit(node.inherit,context)
        context.create_type(node.id)
        for feature in node.features:
            self.visit(feature,context)
        
  @visitor.when(CallTypeAttr)
  def visit(self,node,context):
        self.visit(node.attr,context)

  @visitor.when(TypeInheritNode)
  def visit(self,node,context):
        context.create_type(node.id)

  @visitor.when(AttrDeclarationNode)
  def visit(self,node,context):
        self.visit(node.expr,context)

  @visitor.when(VecInstNode)
  def visit(self,node,context):
        self.visit(node.var,context)
        self.visit(node.index,context)

  @visitor.when(InstantiateTypeNode)
  def visit(self,node,context):
        pass

  @visitor.when(VarsDeclarationsListNode)
  def visit(self,node,context):
        self.visit(node.declarations,context)

  @visitor.when(VarDeclarationNode)
  def visit(self,node,context):
        self.visit(node.expr,context)

  @visitor.when(VarAssignation)
  def visit(self,node,context):
        self.visit(node.expr,context)
        if isinstance(node.id,str) and node.type != 'Object':
                if node.type == node.expr.type:
                    self.errors.append(f'variable {node.id} is not defined')
        else:
            self.visit(node.id,context)

  @visitor.when(WhileLoopNode)
  def visit(self,node,context):
        self.visit(node.expr,context)
        self.visit(node.body,context)

        if node.expr.type != 'Bool':
            self.errors.append(f'can not use {node.expr.type} as Bool')

  @visitor.when(IfNode)
  def visit(self,node,context):
        self.visit(node.if_expr,context)
        self.visit(node.then_expr,context)
        self.visit(node.elsse_expr,context)

        if node.expr.type != 'Bool':
            self.errors.append(f'can not use {node.expr.type} as Bool')

  @visitor.when(CallTypeAttr)
  def visit(self,node,context):
        pass

  @visitor.when(VecInstNode)
  def visit(self,node,context):
        self.visit(node.var,context)
        self.visit(node.index,context)

  @visitor.when(ProtocolNode)
  def visit(self,node,context):
        try:
         context.create_type(node.id)
        except:
            self.errors.append(f'invalid re declaration of {node.id} type')
        if node.extends is not None:
            self.visit(node.extends)